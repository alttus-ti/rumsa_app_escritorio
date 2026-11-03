from datetime import datetime

import requests

from core.database import get_connection
from core.sync_queue import enqueue_sync_event
from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_READ_TIMEOUT_SECONDS,
)


class AltaModel:
    def normalizar_curp(self, curp: str) -> str:
        return (curp or "").strip().upper()

    def buscar_curp_local(self, curp: str):
        curp = self.normalizar_curp(curp)

        if not curp or curp == "-":
            return None

        with get_connection() as connection:
            return connection.execute(
                """
                SELECT p.id, p.nombre, p.curp, t.uid
                FROM pasajeros p
                LEFT JOIN tarjetas t ON t.pasajero_id = p.id
                WHERE UPPER(TRIM(p.curp)) = ?

                UNION ALL

                SELECT o.id, o.nombre, o.curp, t.uid
                FROM operadores o
                JOIN tarjetas t ON t.id = o.tarjeta_id
                WHERE UPPER(TRIM(o.curp)) = ?

                UNION ALL

                SELECT d.id, d.nombre, d.curp, t.uid
                FROM despachadores d
                JOIN tarjetas t ON t.id = d.tarjeta_id
                WHERE UPPER(TRIM(d.curp)) = ?

                LIMIT 1
                """,
                (curp, curp, curp),
            ).fetchone()

    def buscar_curp_servidor(self, curp: str):
        curp = self.normalizar_curp(curp)

        if not curp or curp == "-":
            return None

        response = requests.get(
            f"{SYNC_API_BASE_URL.rstrip('/')}/api/pasajeros/existe-curp",
            params={"curp": curp},
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {SYNC_API_TOKEN}",
                "X-Desktop-Sync-Token": SYNC_API_TOKEN,
            },
            timeout=(
                SYNC_CONNECT_TIMEOUT_SECONDS,
                SYNC_READ_TIMEOUT_SECONDS,
            ),
        )

        response.raise_for_status()
        datos = response.json()

        if datos.get("exists"):
            return datos.get("pasajero") or {"curp": curp}

        return None

    def guardar_alta_local(
        self,
        uid: str,
        nombre_pasajero: str,
        tipo: str,
        vigencia: str,
        curp: str = "",
        fecha_nacimiento="",
        foto: str = "",
    ):
        uid = (uid or "").strip().upper()
        tipo = (tipo or "NO").strip().upper()
        curp = self.normalizar_curp(curp)
        nombre = (nombre_pasajero or "").strip()

        if not uid or not nombre or not curp or curp == "-":
            raise ValueError("Captura UID, nombre y CURP.")

        if tipo not in {"NO", "EU", "KI", "DE"}:
            raise ValueError("Tipo de tarjeta no válido.")

        with get_connection() as connection:
            connection.execute("BEGIN IMMEDIATE")

            if connection.execute(
                "SELECT 1 FROM tarjetas WHERE UPPER(uid) = ?",
                (uid,),
            ).fetchone():
                raise ValueError(
                    "La tarjeta ya existe. Usa sustitución "
                    "si corresponde."
                )

            if connection.execute(
                """
                SELECT 1 FROM pasajeros
                WHERE UPPER(TRIM(curp)) = ?
                UNION ALL
                SELECT 1 FROM operadores
                WHERE UPPER(TRIM(curp)) = ?
                UNION ALL
                SELECT 1 FROM despachadores
                WHERE UPPER(TRIM(curp)) = ?
                LIMIT 1
                """,
                (curp, curp, curp),
            ).fetchone():
                raise ValueError(
                    "La CURP ya existe en la base local."
                )

            clave = {
                "KI": "operador",
                "EU": "preferencial",
                "NO": "normal",
                "DE": "despachador",
            }[tipo]

            tipo_id = connection.execute(
                "SELECT id FROM tipo_tarjetas WHERE clave = ?",
                (clave,),
            ).fetchone()[0]

            pasajero_id = None

            if tipo not in ("KI", "DE"):
                pasajero_id = connection.execute(
                    """
                    INSERT INTO pasajeros (
                        nombre, documento, curp,
                        foto, fecha_nacimiento
                    )
                    VALUES (?, '-', ?, ?, ?)
                    """,
                    (nombre, curp, foto, fecha_nacimiento),
                ).lastrowid

            tarjeta_id = connection.execute(
                """
                INSERT INTO tarjetas (
                    uid, saldo, tipo_tarjeta_id,
                    pasajero_id, vigencia
                )
                VALUES (?, 0, ?, ?, ?)
                """,
                (uid, tipo_id, pasajero_id, vigencia),
            ).lastrowid

            if tipo in ("KI", "DE"):
                tabla = "despachadores" if tipo == "DE" else "operadores"
                connection.execute(
                    f"""
                    INSERT INTO {tabla} (
                        tarjeta_id, nombre, documento,
                        curp, foto, fecha_nacimiento
                    )
                    VALUES (?, ?, '-', ?, ?, ?)
                    """,
                    (
                        tarjeta_id,
                        nombre,
                        curp,
                        foto,
                        fecha_nacimiento,
                    ),
                )

            enqueue_sync_event(
                connection,
                event_type="alta_tarjeta",
                entity_uid=uid,
                payload={
                    "uid": uid,
                    "saldo": 0,
                    "nombre_pasajero": nombre,
                    "documento": "-",
                    "curp": curp,
                    "foto": foto,
                    "fecha_nacimiento": fecha_nacimiento,
                    "tipo_codigo_local": tipo,
                    "entidad": (
                        "despachador" if tipo == "DE"
                        else "operador" if tipo == "KI" else "pasajero"
                    ),
                    "vigencia": vigencia,
                    "local_created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                },
            )

            return tarjeta_id
