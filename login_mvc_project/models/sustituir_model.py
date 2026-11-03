import logging
import re

import requests
from core.database import get_connection
from core.sync_queue import enqueue_sync_event

from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_READ_TIMEOUT_SECONDS,
)


class SustituirModel:
    def __init__(self) -> None:
        self.base_url = SYNC_API_BASE_URL.rstrip("/")
        self.token = SYNC_API_TOKEN.strip()
        self.timeout = (SYNC_CONNECT_TIMEOUT_SECONDS, SYNC_READ_TIMEOUT_SECONDS)
        self.incidencias_busqueda = []
        
    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Desktop-Sync-Token": self.token,
        }

    def _raise_for_status_con_mensaje(self, response: requests.Response) -> None:
        if response.status_code < 400:
            return

        mensaje = ""
        try:
            data = response.json()
            if isinstance(data, dict):
                mensaje = str(data.get("message") or data.get("error") or "").strip()
        except ValueError:
            mensaje = response.text.strip()

        if not mensaje:
            mensaje = f"HTTP {response.status_code}"

        raise RuntimeError(mensaje)
    
    def buscar_tarjetas_locales(self, texto="", limite=50, *, seccion="pasajeros"):
        self._tipos_seccion(seccion)
        self.incidencias_busqueda = []
        termino = "%" + (texto or "").strip() + "%"

        with get_connection() as connection:
            filas = connection.execute(
                """
                SELECT v.*, tt.clave AS tipo_clave
                FROM v_tarjetas_locales v
                JOIN tipo_tarjetas tt ON tt.id = v.tipo_tarjeta_id
                WHERE en_lista_negra = 0
                  AND (
                      nombre_pasajero LIKE ?
                      OR uid LIKE ?
                      OR curp LIKE ?
                  )
                ORDER BY nombre_pasajero, v.id
                """,
                (termino, termino, termino),
            ).fetchall()

        resultados = {}
        for fila in filas:
            item = self._preparar_resultado_busqueda(dict(fila), seccion, "local")
            if item:
                resultados.setdefault(item["uid"], item)
        lista = list(resultados.values())
        return lista if limite is None else lista[:max(0, int(limite))]

    def _tipos_seccion(self, seccion):
        tipos = {"pasajeros": {"NO", "EU"}, "personal": {"KI", "DE"}}
        if seccion not in tipos:
            raise ValueError("Sección de búsqueda no válida.")
        return tipos[seccion]

    def _uid_busqueda(self, uid):
        if not isinstance(uid, str):
            return ""
        normalizada = uid.strip().upper()
        if not re.fullmatch(r"[0-9A-F]{8,20}", normalizada) or len(normalizada) % 2:
            return ""
        return normalizada

    def _tipo_codigo_busqueda(self, item):
        equivalencias = {
            "NO": "NO", "NOR": "NO", "NORMAL": "NO",
            "EU": "EU", "PRE": "EU", "PREFERENCIAL": "EU",
            "KI": "KI", "OPE": "KI", "OPERADOR": "KI",
            "DE": "DE", "DESPACHADOR": "DE",
        }
        codigos = set()
        for campo in ("tipo_codigo_local", "tipo_clave", "tipo_tarjeta", "tipo", "tipo_descripcion"):
            valor = item.get(campo)
            valores = (
                [valor.get(k) for k in ("clave", "codigo", "descripcion", "tipo_codigo_local")]
                if isinstance(valor, dict) else [valor]
            )
            for texto in valores:
                if isinstance(texto, str):
                    codigo = equivalencias.get(texto.strip().upper())
                    if codigo:
                        codigos.add(codigo)
        return next(iter(codigos)) if len(codigos) == 1 else ""

    def _reportar_busqueda(self, origen, uid, motivo):
        self.incidencias_busqueda.append(dict(origen=origen, uid=uid, motivo=motivo))
        logging.getLogger(__name__).warning(
            "Tarjeta excluida de búsqueda [%s], UID=%r: %s", origen, uid, motivo
        )

    def _preparar_resultado_busqueda(self, item, seccion, origen):
        if not isinstance(item, dict):
            self._reportar_busqueda(origen, None, "Registro sin estructura de tarjeta; revisar origen.")
            return None
        uid = self._uid_busqueda(item.get("uid"))
        if not uid:
            self._reportar_busqueda(origen, item.get("uid"), "UID inválida; revisar sin reconstruirla.")
            return None
        codigo = self._tipo_codigo_busqueda(item)
        if not codigo:
            self._reportar_busqueda(origen, item.get("uid"), "Tipo desconocido o contradictorio; revisar origen.")
            return None
        if codigo not in self._tipos_seccion(seccion) or self._esta_en_lista_negra(item):
            return None
        item = self._normalizar_item_busqueda(item)
        item["uid"] = uid
        return item

    def validar_sustitucion_local(
        self,
        uid_anterior,
        uid_nueva,
    ):
        from core.lista_negra_local import bloqueo_local

        anterior = (uid_anterior or "").strip().upper()
        nueva = (uid_nueva or "").strip().upper()

        if not anterior or not nueva or anterior == nueva:
            raise ValueError("Las UID deben ser distintas.")

        with get_connection() as connection:
            if connection.execute(
                "SELECT 1 FROM tarjetas WHERE uid = ?",
                (nueva,),
            ).fetchone():
                raise ValueError(
                    "La tarjeta nueva ya existe localmente."
                )

            vieja = connection.execute(
                """
                SELECT en_lista_negra FROM tarjetas
                WHERE uid = ?
                """,
                (anterior,),
            ).fetchone()

            if vieja and vieja[0]:
                raise ValueError(
                    "La tarjeta anterior está bloqueada."
                )

        if bloqueo_local(nueva):
            raise ValueError(
                "La tarjeta nueva está en lista negra."
            )

        if bloqueo_local(anterior) and not vieja:
            raise ValueError(
                "La tarjeta anterior está en lista negra."
            )

    def guardar_sustitucion_local(
        self,
        *,
        uid_anterior,
        uid_nueva,
        nueva_vigencia,
        nombre_pasajero="",
        tipo_codigo_local="NO",
        datos_original=None,
    ):
        uid_anterior = uid_anterior.strip().upper()
        uid_nueva = uid_nueva.strip().upper()
        tipo_codigo_local = (tipo_codigo_local or "NO").strip().upper()

        if (
            not uid_anterior
            or not uid_nueva
            or uid_anterior == uid_nueva
        ):
            raise ValueError(
                "Las tarjetas deben ser distintas y tener UID."
            )

        datos = datos_original or {}
        tipo_datos = str(
            datos.get("tipo_tarjeta") or datos.get("tipo_codigo_local") or ""
        ).strip().lower()
        if tipo_datos == "de" or "despachador" in tipo_datos:
            tipo_codigo_local = "DE"
        nombre_pasajero = (
            datos.get("nombre_pasajero") or nombre_pasajero
        )

        with get_connection() as connection:
            connection.execute('BEGIN IMMEDIATE')
            anterior = connection.execute(
                """
                SELECT t.*, tt.clave AS tipo_clave
                FROM tarjetas t
                JOIN tipo_tarjetas tt ON tt.id = t.tipo_tarjeta_id
                WHERE t.uid = ?
                """,
                (uid_anterior,),
            ).fetchone()

            if anterior and str(anterior["tipo_clave"]).strip().lower() in ("de", "despachador"):
                tipo_codigo_local = "DE"

            if connection.execute(
                "SELECT 1 FROM tarjetas WHERE uid = ?",
                (uid_nueva,),
            ).fetchone():
                registrada = connection.execute(
                    """
                    SELECT 1 FROM sustituciones
                    WHERE uid_anterior = ? AND uid_nueva = ?
                    """,
                    (uid_anterior, uid_nueva),
                ).fetchone()

                if registrada:
                    return

                raise ValueError(
                    "La tarjeta nueva ya existe localmente."
                )

            if anterior is None:
                clave = {
                    "KI": "operador",
                    "EU": "preferencial",
                    "DE": "despachador",
                }.get(tipo_codigo_local, "normal")

                tipo_id = connection.execute(
                    """
                    SELECT id FROM tipo_tarjetas
                    WHERE clave = ?
                    """,
                    (clave,),
                ).fetchone()[0]

                pasajero_id = None

                if tipo_codigo_local not in ("KI", "DE"):
                    pasajero_id = connection.execute(
                        """
                        INSERT INTO pasajeros (
                            nombre, documento, curp,
                            foto, fecha_nacimiento
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            nombre_pasajero,
                            datos.get("documento") or "-",
                            datos.get("curp") or "",
                            datos.get("foto") or "",
                            datos.get("fecha_nacimiento") or "",
                        ),
                    ).lastrowid

                anterior_id = connection.execute(
                    """
                    INSERT INTO tarjetas (
                        uid, saldo, tipo_tarjeta_id,
                        pasajero_id, vigencia
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        uid_anterior,
                        0 if tipo_codigo_local == "DE" else float(datos.get("saldo") or 0),
                        tipo_id,
                        pasajero_id,
                        datos.get("vigencia"),
                    ),
                ).lastrowid

                if tipo_codigo_local in ("KI", "DE"):
                    tabla = "despachadores" if tipo_codigo_local == "DE" else "operadores"
                    connection.execute(
                        f"""
                        INSERT INTO {tabla} (
                            tarjeta_id, nombre, documento,
                            curp, foto, fecha_nacimiento
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            anterior_id,
                            nombre_pasajero,
                            datos.get("documento") or "-",
                            datos.get("curp") or "",
                            datos.get("foto") or "",
                            datos.get("fecha_nacimiento") or "",
                        ),
                    )

                anterior = connection.execute(
                    "SELECT * FROM tarjetas WHERE uid = ?",
                    (uid_anterior,),
                ).fetchone()

            if anterior["en_lista_negra"]:
                raise ValueError(
                    "La tarjeta anterior está cancelada."
                )

            es_operador = connection.execute(
                """
                SELECT 1 FROM operadores WHERE tarjeta_id = ?
                UNION ALL
                SELECT 1 FROM despachadores WHERE tarjeta_id = ?
                """,
                (anterior["id"], anterior["id"]),
            ).fetchone() is not None

            saldo_transferido = (
                0 if es_operador else anterior["saldo"]
            )

            nueva_id = connection.execute(
                """
                INSERT INTO tarjetas (
                    uid, saldo, tipo_tarjeta_id,
                    pasajero_id, vigencia
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    uid_nueva,
                    saldo_transferido,
                    anterior["tipo_tarjeta_id"],
                    anterior["pasajero_id"],
                    nueva_vigencia,
                ),
            ).lastrowid

            connection.execute(
                """
                UPDATE tarjetas
                SET saldo = 0,
                    en_lista_negra = 1,
                    fecha_baja = datetime('now'),
                    motivo_baja = 'Sustituida'
                WHERE id = ?
                """,
                (anterior["id"],),
            )

            for tabla in ("operadores", "despachadores"):
                connection.execute(
                    f"UPDATE {tabla} SET tarjeta_id = ? WHERE tarjeta_id = ?",
                    (nueva_id, anterior["id"]),
                )

            sustitucion_id = connection.execute(
                """
                INSERT INTO sustituciones (
                    uid_anterior, uid_nueva,
                    nueva_vigencia, saldo_transferido
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    uid_anterior,
                    uid_nueva,
                    nueva_vigencia,
                    saldo_transferido,
                ),
            ).lastrowid

            operation_uuid = enqueue_sync_event(
                connection,
                event_type="sustitucion_tarjeta",
                entity_uid=uid_anterior,
                payload={
                    "uid_anterior": uid_anterior,
                    "uid_nueva": uid_nueva,
                    "nueva_vigencia": nueva_vigencia,
                    "nombre_pasajero": nombre_pasajero,
                    "tipo_codigo_local": tipo_codigo_local,
                    "entidad": (
                        "despachador" if tipo_codigo_local == "DE"
                        else "operador" if es_operador else "pasajero"
                    ),
                    "saldo_transferido": saldo_transferido,
                    "datos_original": dict(datos),
                },
            )

            connection.execute(
                """
                UPDATE sustituciones SET sync_uuid = ?
                WHERE id = ?
                """,
                (operation_uuid, sustitucion_id),
            )
        
    def buscar_tarjetas_por_nombre(
        self,
        texto: str = "",
        limite: int = 50,
        *,
        seccion: str = "pasajeros",
    ):
        self._tipos_seccion(seccion)
        limite = max(0, int(limite))
        termino = (texto or "").strip()
        locales = self.buscar_tarjetas_locales(termino, limite=None, seccion=seccion)
        if not limite:
            return []

        try:
            response = requests.get(
                f"{self.base_url}/api/tarjetas/buscar",
                params={
                    "texto": termino,
                    # Obtener el lote completo de la API antes de aplicar el límite de la lista.
                    "limite": max(50, limite),
                    "incluir_lista_negra": 0,
                },
                headers=self._headers(),
                timeout=self.timeout,
            )

            self._raise_for_status_con_mensaje(response)
            datos = response.json()
            remotos = datos.get("items", []) if isinstance(datos, dict) else []
            if not isinstance(remotos, list):
                raise ValueError("Respuesta de búsqueda sin lista de tarjetas.")

        except (requests.RequestException, RuntimeError, ValueError):
            return locales[:limite]

        with get_connection() as connection:
            filas = connection.execute("""
                SELECT v.*, tt.clave AS tipo_clave
                FROM v_tarjetas_locales v
                JOIN tipo_tarjetas tt ON tt.id = v.tipo_tarjeta_id
                ORDER BY v.id
            """).fetchall()
        conocidos = {}
        for fila in filas:
            uid = self._uid_busqueda(fila["uid"])
            if uid:
                conocidos.setdefault(uid, dict(fila))
        resultados = {item["uid"]: item for item in locales}
        for remoto in remotos:
            if not isinstance(remoto, dict) or not self._uid_busqueda(remoto.get("uid")):
                self._preparar_resultado_busqueda(remoto, seccion, "servidor")
                continue
            uid = self._uid_busqueda(remoto["uid"])
            if uid in resultados:
                continue
            # El servidor nunca reemplaza el tipo, datos o bloqueo de una UID local.
            origen = "local" if uid in conocidos else "servidor"
            item = self._preparar_resultado_busqueda(conocidos.get(uid, remoto), seccion, origen)
            if item:
                resultados[uid] = item
        return list(resultados.values())[:limite]
    
    
    def _esta_en_lista_negra(self, item: dict) -> bool:
        if not isinstance(item, dict):
            return False

        pasajero = item.get("pasajero")
        if not isinstance(pasajero, dict):
            pasajero = {}

        for value in (
            item.get("en_lista_negra"),
            item.get("lista_negra"),
            item.get("bloqueada"),
            pasajero.get("en_lista_negra"),
            pasajero.get("lista_negra"),
            pasajero.get("bloqueada"),
        ):
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return value == 1

            texto = str(value or "").strip().lower()
            if texto in {"1", "true", "si", "yes", "y"}:
                return True

        return False

    def _normalizar_item_busqueda(self, item: dict) -> dict:
        if not isinstance(item, dict):
            return {}

        pasajero = item.get("pasajero")
        if not isinstance(pasajero, dict):
            pasajero = {}

        item = dict(item)
        codigo = self._tipo_codigo_busqueda(item)
        item["tipo_codigo_local"] = codigo
        item["tipo_tarjeta"] = {
            "NO": "Normal", "EU": "Preferencial", "KI": "Operador", "DE": "Despachador"
        }.get(codigo, "Desconocido")
        item["documento"] = (
            item.get("documento")
            or item.get("documento_pasajero")
            or pasajero.get("documento")
            or "-"
        )
        item["curp"] = (
            item.get("curp")
            or item.get("curp_pasajero")
            or pasajero.get("curp")
            or ""
        )
        item["fecha_nacimiento"] = (
            item.get("fecha_nacimiento")
            or item.get("fecha_nacimiento_pasajero")
            or pasajero.get("fecha_nacimiento")
            or ""
        )
        return item
    
    def sustituir_tarjeta(
        self,
        *,
        uid_anterior: str,
        uid_nueva: str,
        nueva_vigencia: str,
    ):
        payload = {
            "uid_anterior": (uid_anterior or "").strip().upper(),
            "uid_nueva": (uid_nueva or "").strip().upper(),
            "nueva_vigencia": (nueva_vigencia or "").strip(),
        }
        response = requests.post(
            f"{self.base_url}/api/tarjetas/sustituir",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("ok", False):
            raise ValueError(data.get("message", "No se pudo sustituir la tarjeta."))

        return data
    
    def sustituir_tarjeta_servidor(
        self,
        *,
        uid_anterior: str,
        uid_nueva: str,
        nueva_vigencia: str,
        nombre_pasajero: str = "",
        tipo_codigo_local: str | None = None,
    ):
        payload = {
            "uid_anterior": (uid_anterior or "").strip().upper(),
            "uid_nueva": (uid_nueva or "").strip().upper(),
            "nueva_vigencia": (nueva_vigencia or "").strip(),
            "nombre_pasajero": (nombre_pasajero or "").strip(),
            "tipo_codigo_local": (tipo_codigo_local or "NO").strip().upper(),
        }

        response = requests.post(
            f"{self.base_url}/api/tarjetas/sustituir",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        )
        self._raise_for_status_con_mensaje(response)
        data = response.json()

        if not data.get("ok", False):
            raise ValueError(data.get("message", "No se pudo sustituir la tarjeta."))

        return data
