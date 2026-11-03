from __future__ import annotations

import json
import uuid
from typing import Any


def enqueue_sync_event(
    connection,
    *,
    event_type: str,
    entity_uid: str | None,
    payload: dict[str, Any],
) -> str:
    payload = dict(payload)

    titular = connection.execute(
        """
        SELECT tipo_tarjeta, entidad
        FROM v_tarjetas_locales
        WHERE uid = ?
        LIMIT 1
        """,
        (entity_uid,),
    ).fetchone()

    if titular:
        payload.setdefault("entidad", titular["entidad"])
    tipo = str(
        titular["tipo_tarjeta"] if titular
        else payload.get("tipo_codigo_local") or ""
    ).strip().lower()

    if tipo == "de" or "despachador" in tipo:
        payload["entidad"] = "despachador"
        payload["tipo_codigo_local"] = "DE"

    elif tipo in {"ki", "ope"} or "operador" in tipo:
        payload["entidad"] = "operador"
        payload["tipo_codigo_local"] = "KI"

    operation_uuid = str(uuid.uuid4())

    connection.execute(
        """
        INSERT INTO sync_queue (
            operation_uuid, event_type, entity_uid,
            payload_json, status, retries, last_error
        )
        VALUES (?, ?, ?, ?, 'pending', 0, NULL)
        """,
        (
            operation_uuid,
            event_type,
            entity_uid,
            json.dumps(payload, ensure_ascii=False),
        ),
    )

    return operation_uuid
