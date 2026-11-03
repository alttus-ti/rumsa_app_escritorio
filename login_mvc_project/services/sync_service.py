from __future__ import annotations

import json
import time
from pathlib import Path

import requests

from core.database import get_connection, DATABASE_DIR
from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_BATCH_PATH,
    SYNC_BATCH_SIZE,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_READ_TIMEOUT_SECONDS,
    SYNC_PING_PATH,
    SYNC_UPLOAD_FOTO_PATH,
)


class SyncService:
    def __init__(self):
        self.base_url = SYNC_API_BASE_URL.rstrip("/")
        self.token = SYNC_API_TOKEN.strip()
        self.timeout = (
            SYNC_CONNECT_TIMEOUT_SECONDS,
            SYNC_READ_TIMEOUT_SECONDS,
        )
        self._last_blacklist = 0

    def _headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Desktop-Sync-Token": self.token,
        }

    def count_pending(self):
        with get_connection() as c:
            return c.execute(
                """
                SELECT COUNT(*) FROM sync_queue
                WHERE status IN ('pending', 'error', 'waiting_api')
                """
            ).fetchone()[0]

    def _ping_data(self):
        r = requests.get(
            f"{self.base_url}{SYNC_PING_PATH}",
            headers=self._headers(),
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def hay_internet(self):
        try:
            return bool(self._ping_data().get("ok"))
        except (requests.RequestException, ValueError):
            return False

    def ping(self):
        return self.hay_internet()

    def sync_pending_once(self):
        before = self.count_pending()
        synced = 0
        errors = 0
        message = "Sin pendientes"
        try:
            data = self._ping_data()
            if not isinstance(data, dict) or not data.get("ok"):
                raise ValueError("La API no confirmo la conexion.")
            capabilities = data.get("capabilities") or []
            if not isinstance(capabilities, list):
                capabilities = []

            if time.monotonic() - self._last_blacklist > 300:
                try:
                    self._refresh_blacklist()
                    self._last_blacklist = time.monotonic()
                except Exception as error:
                    message = f"Se conserva la lista negra anterior: {error}"
                    errors += 1

            with get_connection() as c:
                rows = c.execute("""
                    SELECT * FROM sync_queue
                    WHERE status IN ('pending', 'error', 'waiting_api')
                    ORDER BY id
                """).fetchall()

            blocked_uids = set()
            for row in rows:
                if synced >= SYNC_BATCH_SIZE:
                    break
                try:
                    payload = json.loads(row["payload_json"])
                    if not isinstance(payload, dict):
                        raise ValueError("Payload de sincronizacion invalido.")
                except (ValueError, TypeError) as error:
                    self._mark_error(row["operation_uuid"], str(error))
                    blocked_uids.add(str(row["entity_uid"] or "").strip().upper())
                    errors += 1
                    message = str(error)
                    continue
                operation = {
                    "operation_uuid": row["operation_uuid"],
                    "event_type": row["event_type"],
                    "entity_uid": row["entity_uid"],
                    "payload": payload,
                }
                uids = self._operation_uids(operation)
                if uids & blocked_uids:
                    blocked_uids.update(uids)
                    continue
                incompatibilidad = self._compatibility_error(operation, capabilities)
                if incompatibilidad:
                    self._mark_waiting_api(operation["operation_uuid"], incompatibilidad)
                    blocked_uids.update(uids)
                    errors += 1
                    message = incompatibilidad
                    continue
                try:
                    self._prepare_photo(operation)
                except Exception as error:
                    self._mark_error(operation["operation_uuid"], str(error))
                    blocked_uids.update(uids)
                    errors += 1
                    message = str(error)
                    continue

                # Una sola operacion por peticion: confirmar antes de continuar.
                response = requests.post(
                    f"{self.base_url}{SYNC_BATCH_PATH}",
                    json={"operations": [operation]},
                    headers=self._headers(),
                    timeout=self.timeout,
                )
                response.raise_for_status()
                body = response.json()
                results = body.get("results", []) if isinstance(body, dict) else []
                if not isinstance(results, list):
                    results = []
                matches = [item for item in results if isinstance(item, dict)
                           and item.get("operation_uuid") == operation["operation_uuid"]]
                if len(matches) != 1:
                    errors += 1
                    message = "Operacion sin confirmacion unica; se conserva pendiente."
                    break
                result = matches[0]
                if result.get("status") not in {"ok", "already_synced"}:
                    message = result.get("message") or "Error de sincronizacion."
                    self._mark_error(operation["operation_uuid"], message)
                    blocked_uids.update(uids)
                    errors += 1
                    continue

                self._mark_synced(operation["operation_uuid"])
                synced += 1

            self._maintenance()
            if synced and not errors:
                message = "Sincronizacion completada"
            return self._result("connected_with_errors" if errors else "connected",
                                before, synced, errors, message)
        except Exception as error:
            return self._result("offline", before, synced, errors, str(error))

    def _operation_uids(self, operation):
        payload = operation["payload"]
        return {str(uid).strip().upper() for uid in (
            operation.get("entity_uid"), payload.get("uid"),
            payload.get("uid_anterior"), payload.get("uid_nueva")) if uid}

    def _compatibility_error(self, operation, capabilities):
        payload = operation["payload"]
        tipo = str(payload.get("tipo_codigo_local") or "").strip().upper()
        tipo = {"NORMAL": "NO", "NOR": "NO", "PREFERENCIAL": "EU", "PRE": "EU",
                "OPERADOR": "KI", "OPE": "KI", "DESPACHADOR": "DE"}.get(tipo, tipo)
        entidad = payload.get("entidad")
        if entidad == "despachador":
            tipo = "DE"
        elif entidad == "operador" and tipo != "DE":
            tipo = "KI"
        if tipo and tipo not in {"NO", "EU", "KI", "DE"}:
            return "Tipo de tarjeta no compatible; se conserva pendiente."
        if tipo not in {"KI", "DE"}:
            with get_connection() as c:
                for uid in self._operation_uids(operation):
                    tarjeta = c.execute(
                        "SELECT tipo_tarjeta FROM v_tarjetas_locales WHERE uid=? LIMIT 1", (uid,)
                    ).fetchone()
                    descripcion = str(tarjeta[0] or "").lower() if tarjeta else ""
                    if descripcion == "de" or "despachador" in descripcion:
                        tipo = "DE"
                        break
                    if descripcion in {"ki", "ope"} or "operador" in descripcion:
                        tipo = "KI"
                        break
        if operation["event_type"] == "recarga_tarjeta" and tipo in {"KI", "DE"}:
            return "Las tarjetas de operador y despachador no admiten recargas."
        if tipo == "DE" and "despachadores_offline_v1" not in capabilities:
            return "La API requiere soporte para DE/despachador; el evento sigue pendiente."
        if tipo == "KI" and "operadores_offline_v1" not in capabilities:
            return "La API requiere soporte para KI/operador; el evento sigue pendiente."
        if (operation["event_type"] == "sustitucion_tarjeta"
                and "sustituciones_offline_v1" not in capabilities):
            return "La API requiere soporte para sustituciones; el evento sigue pendiente."
        if operation["event_type"] not in {
                "alta_tarjeta", "recarga_tarjeta", "cancelacion_tarjeta", "sustitucion_tarjeta"}:
            return "Tipo de evento no compatible; se conserva pendiente."
        return ""

    def _mark_waiting_api(self, operation_uuid, message):
        with get_connection() as c:
            c.execute("""
                UPDATE sync_queue SET status='waiting_api', last_error=?
                WHERE operation_uuid=?
            """, (message, operation_uuid))

    def _result(
        self,
        state,
        before,
        synced,
        errors,
        message,
    ):
        return {
            "state": state,
            "pending_before": before,
            "pending_after": self.count_pending(),
            "synced_count": synced,
            "error_count": errors,
            "message": message,
        }

    def _prepare_photo(self, operation):
        if operation["event_type"] != "alta_tarjeta":
            return

        payload = operation["payload"]
        foto = str(payload.get("foto") or "")

        prefijos = (
            "pasajeros/",
            "operadores/",
            "despachadores/",
            "http://",
            "https://",
        )

        if not foto or foto.startswith(prefijos):
            return

        path = Path(foto)

        if not path.is_file():
            raise ValueError(
                "La foto pendiente no está disponible: "
                f"{path.name}"
            )

        with path.open("rb") as file:
            r = requests.post(
                f"{self.base_url}{SYNC_UPLOAD_FOTO_PATH}",
                headers=self._headers(),
                data={"uid": payload["uid"]},
                files={"foto": (path.name, file)},
                timeout=self.timeout,
            )

        r.raise_for_status()
        data = r.json()

        if not data.get("ok") or not data.get("path"):
            raise ValueError("No se confirmó la foto.")

        payload["foto"] = data["path"]

        with get_connection() as c:
            c.execute(
                """
                UPDATE sync_queue SET payload_json = ?
                WHERE operation_uuid = ?
                """,
                (
                    json.dumps(payload, ensure_ascii=False),
                    operation["operation_uuid"],
                ),
            )

    def _mark_synced(self, operation_uuid):
        prefijos = (
            "pasajeros/",
            "operadores/",
            "despachadores/",
            "http://",
            "https://",
        )

        with get_connection() as c:
            row = c.execute(
                """
                SELECT event_type, entity_uid, payload_json
                FROM sync_queue
                WHERE operation_uuid = ?
                """,
                (operation_uuid,),
            ).fetchone()

            if row and row["event_type"] == "alta_tarjeta":
                remote = str(
                    json.loads(row["payload_json"]).get("foto")
                    or ""
                )

                if remote.startswith(prefijos):
                    titulares = (
                        (
                            "pasajeros",
                            "id IN (SELECT pasajero_id "
                            "FROM tarjetas WHERE uid = ?)",
                        ),
                        (
                            "operadores",
                            "tarjeta_id IN (SELECT id "
                            "FROM tarjetas WHERE uid = ?)",
                        ),
                        (
                            "despachadores",
                            "tarjeta_id IN (SELECT id "
                            "FROM tarjetas WHERE uid = ?)",
                        ),
                    )

                    for table, condition in titulares:
                        old = c.execute(
                            f"SELECT foto FROM {table} "
                            f"WHERE {condition}",
                            (row["entity_uid"],),
                        ).fetchall()

                        for foto in old:
                            local = str(foto[0] or "")

                            if (
                                local
                                and not local.startswith(prefijos)
                            ):
                                c.execute(
                                    """
                                    INSERT OR REPLACE
                                    INTO uploaded_photos
                                    VALUES (?, ?)
                                    """,
                                    (local, remote),
                                )

                        c.execute(
                            f"UPDATE {table} SET foto = ? "
                            f"WHERE {condition}",
                            (remote, row["entity_uid"]),
                        )

            for table in ("recargas", "sustituciones"):
                c.execute(
                    f"""
                    UPDATE {table}
                    SET sincronizada = 1,
                        synced_at = datetime('now')
                    WHERE sync_uuid = ?
                    """,
                    (operation_uuid,),
                )

            c.execute(
                """
                DELETE FROM sync_queue
                WHERE operation_uuid = ?
                """,
                (operation_uuid,),
            )

    def _mark_error(self, operation_uuid, message):
        with get_connection() as c:
            c.execute(
                """
                UPDATE sync_queue
                SET status = 'error',
                    retries = retries + 1,
                    last_error = ?
                WHERE operation_uuid = ?
                """,
                (str(message)[:1000], operation_uuid),
            )

    def _refresh_blacklist(self):
        after = 0

        with get_connection() as c:
            c.execute("DELETE FROM blacklist_stage")

        while True:
            r = requests.get(
                f"{self.base_url}/api/desktop-sync/blacklist",
                params={"after_id": after},
                headers=self._headers(),
                timeout=self.timeout,
            )

            r.raise_for_status()
            data = r.json()

            if (
                not data.get("ok")
                or not isinstance(data.get("items"), list)
                or 'next_after_id' not in data
            ):
                raise ValueError(
                    "Respuesta de lista negra incompleta."
                )

            with get_connection() as c:
                for row in data["items"]:
                    uid = str(row["uid"]).strip().upper()

                    if not uid:
                        raise ValueError(
                            "UID vacía en lista negra."
                        )

                    c.execute(
                        """
                        INSERT OR REPLACE INTO blacklist_stage (
                            uid, motivo, fecha_baja
                        )
                        VALUES (?, ?, ?)
                        """,
                        (
                            uid,
                            str(
                                row.get("motivo_baja") or ""
                            )[:250],
                            row.get("fecha_baja"),
                        ),
                    )

            next_after = data.get("next_after_id")

            if next_after is None:
                break

            if int(next_after) <= after:
                raise ValueError(
                    "Paginación de lista negra inválida."
                )

            after = int(next_after)

        with get_connection() as c:
            c.execute("DELETE FROM lista_negra")

            c.execute(
                """
                INSERT INTO lista_negra
                SELECT uid, motivo, fecha_baja
                FROM blacklist_stage
                """
            )

            c.execute("DELETE FROM blacklist_stage")

            c.execute(
                """
                INSERT OR REPLACE INTO local_settings
                VALUES (
                    'blacklist_updated_at',
                    datetime('now')
                )
                """
            )

            c.execute(
                """
                UPDATE tarjetas
                SET en_lista_negra = CASE
                    WHEN EXISTS (
                        SELECT 1 FROM lista_negra b
                        WHERE b.uid = tarjetas.uid
                    )
                    THEN 1
                    ELSE 0
                END,
                motivo_baja = (
                    SELECT motivo FROM lista_negra b
                    WHERE b.uid = tarjetas.uid
                ),
                fecha_baja = (
                    SELECT fecha_baja FROM lista_negra b
                    WHERE b.uid = tarjetas.uid
                )
                WHERE NOT EXISTS (
                    SELECT 1 FROM sync_queue q
                    WHERE q.entity_uid = tarjetas.uid
                      AND q.status IN (
                          'pending', 'error', 'waiting_api'
                      )
                )
                """
            )

    def _maintenance(self):
        # Solo consolidar el WAL; conservar todo el historial y las fotos.
        with get_connection() as c:
            c.execute("PRAGMA wal_checkpoint(PASSIVE)")

    def limpiar_tarjetas_locales_ya_subidas(self):
        return 0
