from datetime import datetime
from core.lista_negra_local import bloqueo_local

import requests

from core.database import get_connection
from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_READ_TIMEOUT_SECONDS,
)
from core.sync_queue import enqueue_sync_event


class CancelarModel:
    def __init__(self) -> None:
        self.base_url = SYNC_API_BASE_URL.rstrip("/")
        self.token = SYNC_API_TOKEN.strip()
        self.timeout = (SYNC_CONNECT_TIMEOUT_SECONDS, SYNC_READ_TIMEOUT_SECONDS)

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

        local = self._obtener_tarjeta_local_por_uid(uid)
        if local:
            return local
        bloqueo = bloqueo_local(uid)
        if bloqueo:
            return bloqueo
        tarjeta_servidor = self._obtener_tarjeta_servidor_por_uid(uid)
        if tarjeta_servidor:
            return tarjeta_servidor

        return self._obtener_tarjeta_local_por_uid(uid)

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
            return tarjeta

    def _obtener_tarjeta_servidor_por_uid(self, uid: str):
        if not self.base_url or not self.token:
            return None

        try:
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
        except Exception as error:
            print(f"[CANCELAR] No se pudo consultar tarjeta en servidor: {error}")
            return None

        for item in data.get("items", []):
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
            primero("tipo_tarjeta", "tipo", "tipo_descripcion", "tipo_codigo_local", default="")
        ).strip()
        if tipo_tarjeta.upper() == "DE" or "despachador" in tipo_tarjeta.lower():
            tipo_tarjeta = "Despachador"

        return {
            "id": None,
            "uid": str(primero("uid", default="")).strip().upper(),
            "saldo": float(primero("saldo", "saldo_actual", default=0) or 0),
            "vigencia": primero("vigencia", "fecha_vigencia", default=None),
            "en_lista_negra": 1 if como_bool(
                primero("en_lista_negra", "lista_negra", "bloqueada", default=False)
            ) else 0,
            "motivo_baja": str(
                primero("motivo_baja", "motivo", "motivo_lista_negra", default="")
            ).strip(),
            "fecha_baja": primero("fecha_baja", default=None),
            "pasajero_id": None,
            "tipo_tarjeta": tipo_tarjeta,
            "nombre_pasajero": str(
                primero("nombre_pasajero", "nombre", "pasajero", default="")
            ).strip(),
        }

    def _asegurar_tarjeta_local(
        self,
        connection,
        uid: str,
        nombre_pasajero: str = "",
        saldo_actual: float = 0.0,
        tipo_codigo_local: str = "",
    ):
        tarjeta = connection.execute(
            """
            SELECT id, pasajero_id
            FROM tarjetas
            WHERE uid = ?
            LIMIT 1
            """,
            (uid,),
        ).fetchone()

        nombre_final = (
            (nombre_pasajero or "").strip()
            or f"Tarjeta {uid[-4:]}"
        )

        if tarjeta:
            if (
                tarjeta["pasajero_id"]
                and nombre_pasajero.strip()
            ):
                connection.execute(
                    """
                    UPDATE pasajeros SET nombre = ?
                    WHERE id = ?
                    """,
                    (nombre_final, tarjeta["pasajero_id"]),
                )

            if nombre_pasajero.strip():
                for tabla in ("operadores", "despachadores"):
                    connection.execute(
                        f"UPDATE {tabla} SET nombre = ? WHERE tarjeta_id = ?",
                        (nombre_final, tarjeta["id"]),
                    )

            return tarjeta["id"]

        if tipo_codigo_local not in {"KI", "NO", "EU", "DE"}:
            raise ValueError(
                "Lee de nuevo la tarjeta para identificar "
                "su tipo antes de cancelarla."
            )

        clave = {
            "KI": "operador",
            "EU": "preferencial",
            "DE": "despachador",
        }.get(tipo_codigo_local, "normal")

        tipo_id = connection.execute(
            "SELECT id FROM tipo_tarjetas WHERE clave = ?",
            (clave,),
        ).fetchone()[0]

        pasajero_id = None

        if tipo_codigo_local not in ("KI", "DE"):
            pasajero_id = connection.execute(
                """
                INSERT INTO pasajeros(nombre, documento)
                VALUES (?, '-')
                """,
                (nombre_final,),
            ).lastrowid

        tarjeta_id = connection.execute(
            """
            INSERT INTO tarjetas (
                uid, saldo, tipo_tarjeta_id,
                pasajero_id, vigencia, en_lista_negra
            )
            VALUES (?, ?, ?, ?, NULL, 0)
            """,
            (
                uid,
                float(saldo_actual or 0),
                tipo_id,
                pasajero_id,
            ),
        ).lastrowid

        if tipo_codigo_local in ("KI", "DE"):
            tabla = "despachadores" if tipo_codigo_local == "DE" else "operadores"
            connection.execute(
                f"""
                INSERT INTO {tabla}(tarjeta_id, nombre)
                VALUES (?, ?)
                """,
                (tarjeta_id, nombre_final),
            )

        return tarjeta_id
    
    def guardar_lectura_si_no_existe(
        self,
        uid: str,
        nombre_pasajero: str = "",
        saldo_actual: float = 0.0,
    ):
        with get_connection() as connection:
            return self._asegurar_tarjeta_local(
                connection=connection,
                uid=uid,
                nombre_pasajero=nombre_pasajero,
                saldo_actual=saldo_actual,
            )

    def cancelar_tarjeta_flexible(
        self,
        uid: str,
        nombre_pasajero: str = "",
        saldo_actual: float = 0.0,
        en_lista_negra: bool = True,
        motivo_baja: str = "Cancelada",
        tipo_codigo_local: str = "",
    ):
        uid = (uid or "").strip().upper()
        tipo_codigo_local = (tipo_codigo_local or "").strip().upper()

        with get_connection() as connection:
            connection.execute('BEGIN IMMEDIATE')
            tarjeta_id = self._asegurar_tarjeta_local(
                connection=connection,
                uid=uid,
                nombre_pasajero=nombre_pasajero,
                saldo_actual=saldo_actual,
                tipo_codigo_local=tipo_codigo_local,
            )

            fecha_baja = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if en_lista_negra
                else None
            )

            motivo_final = (
                motivo_baja if en_lista_negra else None
            )

            connection.execute(
                """
                UPDATE tarjetas
                SET en_lista_negra = ?,
                    motivo_baja = ?,
                    fecha_baja = ?
                WHERE id = ?
                """,
                (
                    int(en_lista_negra),
                    motivo_final,
                    fecha_baja,
                    tarjeta_id,
                ),
            )

            enqueue_sync_event(
                connection,
                event_type="cancelacion_tarjeta",
                entity_uid=uid,
                payload={
                    "uid": uid,
                    "nombre_pasajero": (
                        nombre_pasajero or ""
                    ).strip(),
                    "saldo_actual": float(saldo_actual or 0),
                    "en_lista_negra": bool(en_lista_negra),
                    "motivo_baja": motivo_final,
                    "fecha_baja": fecha_baja,
                },
            )

            return tarjeta_id
