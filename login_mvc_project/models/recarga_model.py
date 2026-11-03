from datetime import datetime
from time import monotonic

import json

from core.lista_negra_local import bloqueo_local

import requests

from core.database import get_connection
from core.sync_queue import enqueue_sync_event
from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_READ_TIMEOUT_SECONDS,
)


class RecargaModel:
    def __init__(self) -> None:
        self.base_url = SYNC_API_BASE_URL.rstrip("/")
        self.token = SYNC_API_TOKEN.strip()
        self.timeout = (SYNC_CONNECT_TIMEOUT_SECONDS, SYNC_READ_TIMEOUT_SECONDS)
        self._cache_tarjetas_servidor = {}

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Desktop-Sync-Token": self.token,
        }
        
        
    def obtener_tarjeta_por_uid(self, uid: str):
        uid = (uid or "").strip().upper()

        if not uid:
            return None

        tarjeta_local = self._obtener_tarjeta_local_por_uid(uid)

        if tarjeta_local:
            with get_connection() as connection:
                pendiente = connection.execute(
                    """
                    SELECT 1 FROM sync_queue
                    WHERE entity_uid = ?
                      AND status IN ('pending', 'error', 'waiting_api')
                    LIMIT 1
                    """,
                    (uid,),
                ).fetchone()

            if tarjeta_local["en_lista_negra"] or pendiente:
                return tarjeta_local

        tarjeta_servidor = (
            self._obtener_tarjeta_servidor_por_uid(uid)
        )

        return tarjeta_servidor or tarjeta_local

    def _obtener_tarjeta_local_por_uid(self, uid: str):
        with get_connection() as connection:
            tarjeta = connection.execute(
                """
                SELECT * FROM v_tarjetas_locales
                WHERE uid = ?
                LIMIT 1
                """,
                (uid,),
            ).fetchone()

        return tarjeta or bloqueo_local(uid)
    
    
    def _obtener_tarjeta_servidor_por_uid(self, uid: str):
        if not self.base_url or not self.token:
            return None

        ahora = monotonic()
        cache = self._cache_tarjetas_servidor.get(uid)
        if cache and ahora - cache["time"] < 5:
            return cache["data"]

        try:
            tarjeta = self._consultar_tarjeta_servidor(uid)
        except Exception as error:
            print(f"[RECARGA] No se pudo consultar tarjeta en servidor: {error}")
            tarjeta = None

        self._cache_tarjetas_servidor[uid] = {
            "time": ahora,
            "data": tarjeta,
        }
        return tarjeta

    def _consultar_tarjeta_servidor(self, uid: str):
        response = requests.get(
            f"{self.base_url}/api/tarjetas/buscar",
            params={
                "texto": uid,
                "limite": 5,
                "incluir_lista_negra": 1,
            },
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        for item in items:
            if not isinstance(item, dict):
                continue

            if str(item.get("uid") or "").strip().upper() == uid:
                return self._normalizar_tarjeta_servidor(item)

        return None

    def _normalizar_tarjeta_servidor(self, item: dict):
        def primero(*keys, default=None):
            for key in keys:
                value = item.get(key)
                if value is not None and value != "":
                    return value
            return default

        def como_bool(value) -> bool:
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return value == 1

            texto = str(value or "").strip().lower()
            return texto in {"1", "true", "si", "yes", "y"}

        tipo_tarjeta = str(
            primero("tipo_tarjeta", "tipo", "tipo_descripcion", "tipo_codigo_local", default="Normal")
        ).strip() or "Normal"
        if tipo_tarjeta.upper() == "DE" or "despachador" in tipo_tarjeta.lower():
            tipo_tarjeta = "Despachador"

        return {
            "uid": str(primero("uid", default="")).strip().upper(),
            "saldo": float(primero("saldo", "saldo_actual", default=0) or 0),
            "vigencia": primero("vigencia", "fecha_vigencia", default=None),
            "tipo_tarjeta": tipo_tarjeta,
            "tipo_tarjeta_id": (
                primero("tipo_tarjeta_id", default=None)
                if tipo_tarjeta == "Despachador"
                else (2 if "prefer" in tipo_tarjeta.lower() else 1)
            ),
            "nombre_pasajero": str(
                primero("nombre_pasajero", "nombre", "pasajero", default="")
            ).strip(),
            "en_lista_negra": 1 if como_bool(
                primero("en_lista_negra", "lista_negra", "bloqueada", default=False)
            ) else 0,
            "motivo_baja": str(
                primero("motivo_baja", "motivo", "motivo_lista_negra", default="")
            ).strip(),
        }

    def _obtener_usuario_id(self, connection, username: str):
        row = connection.execute(
            "SELECT id FROM usuarios WHERE username = ? LIMIT 1",
            (username,),
        ).fetchone()

        if row is None:
            raise ValueError("El usuario no existe en la base local.")

        return row["id"]

    def _asegurar_tarjeta_local(
        self,
        connection,
        uid: str,
        nombre_pasajero: str,
        saldo_actual: float,
    ):
        tarjeta = connection.execute(
            "SELECT id FROM tarjetas WHERE uid = ? LIMIT 1",
            (uid,),
        ).fetchone()

        if tarjeta:
            connection.execute(
                "UPDATE tarjetas SET saldo = ? WHERE id = ?",
                (saldo_actual, tarjeta["id"]),
            )
            return tarjeta["id"]

        nombre_final = (nombre_pasajero or "").strip()
        if not nombre_final:
            nombre_final = f"Tarjeta {uid[-4:]}"

        documento_auto = "-"


        cursor_pasajero = connection.execute(
            """
            INSERT INTO pasajeros (nombre, documento)
            VALUES (?, ?)
            """,
            (nombre_final, documento_auto),
        )
        pasajero_id = cursor_pasajero.lastrowid

        cursor_tarjeta = connection.execute(
            """
            INSERT INTO tarjetas (uid, saldo, tipo_tarjeta_id, pasajero_id, vigencia)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                uid,
                saldo_actual,
                1,
                pasajero_id,
                None,
            ),
        )
        return cursor_tarjeta.lastrowid

    def guardar_recarga_flexible(
        self,
        uid: str,
        username: str,
        monto: float,
        nuevo_saldo: float,
        nombre_pasajero: str = "",
        oficina: str = "",
        referencia: str | None = None,
    ):
        uid = (uid or "").strip().upper()

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        nombre_final = (
            (nombre_pasajero or "").strip()
            or f"Tarjeta {uid[-4:]}"
        )

        with get_connection() as connection:
            connection.execute('BEGIN IMMEDIATE')
            tarjeta = connection.execute(
                """
                SELECT
                    tt.clave,
                    tt.descripcion,
                    t.en_lista_negra
                FROM tarjetas t
                JOIN tipo_tarjetas tt
                    ON tt.id = t.tipo_tarjeta_id
                WHERE UPPER(t.uid) = ?
                LIMIT 1
                """,
                (uid,),
            ).fetchone()

            if tarjeta:
                clave = str(tarjeta["clave"] or "").lower()
                descripcion = str(
                    tarjeta["descripcion"] or ""
                ).lower()

                if (
                    clave in {"ki", "ope", "operador", "de", "despachador"}
                    or "operador" in descripcion
                    or "despachador" in descripcion
                ):
                    raise ValueError(
                        "Las tarjetas de Despachador no admiten recargas."
                        if clave in {"de", "despachador"} or "despachador" in descripcion
                        else "Las tarjetas de operador no admiten recargas."
                    )
                if tarjeta["en_lista_negra"]:
                    raise ValueError(
                        "La tarjeta está en lista negra."
                    )

            if bloqueo_local(uid):
                pendiente = connection.execute(
                    """
                    SELECT payload_json
                    FROM sync_queue
                    WHERE entity_uid = ?
                      AND event_type = 'cancelacion_tarjeta'
                      AND status IN ('pending', 'error')
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (uid,),
                ).fetchone()

                reactivada_localmente = (
                    pendiente is not None
                    and not json.loads(
                        pendiente["payload_json"]
                    ).get("en_lista_negra", True)
                )

                if not reactivada_localmente:
                    raise ValueError(
                        "La tarjeta está en lista negra."
                    )

            usuario_id = self._obtener_usuario_id(
                connection,
                username,
            )

            tarjeta_id = self._asegurar_tarjeta_local(
                connection=connection,
                uid=uid,
                nombre_pasajero=nombre_pasajero,
                saldo_actual=nuevo_saldo,
            )

            recarga_id = connection.execute(
                """
                INSERT INTO recargas (
                    tarjeta_id,
                    usuario_id,
                    monto,
                    oficina,
                    referencia
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    tarjeta_id,
                    usuario_id,
                    monto,
                    oficina,
                    referencia,
                ),
            ).lastrowid

            operation_uuid = enqueue_sync_event(
                connection,
                event_type="recarga_tarjeta",
                entity_uid=uid,
                payload={
                    "uid": uid,
                    "username": username,
                    "monto": float(monto),
                    "nuevo_saldo": float(nuevo_saldo),
                    "nombre_pasajero": nombre_final,
                    "documento": "",
                    "oficina": oficina,
                    "referencia": referencia,
                    "local_created_at": created_at,
                },
            )

            connection.execute(
                """
                UPDATE recargas SET sync_uuid = ?
                WHERE id = ?
                """,
                (operation_uuid, recarga_id),
            )
