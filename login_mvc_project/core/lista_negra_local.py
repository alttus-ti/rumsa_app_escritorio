from core.database import get_connection


def bloqueo_local(uid):
    uid = (uid or '').strip().upper()
    with get_connection() as connection:
        local = connection.execute(
            "SELECT * FROM v_tarjetas_locales WHERE uid = ? LIMIT 1", (uid,)
        ).fetchone()
        if local and local['en_lista_negra']:
            return dict(local)
        pendiente = connection.execute(
            """SELECT 1 FROM sync_queue WHERE entity_uid = ?
               AND event_type = 'cancelacion_tarjeta'
               AND status IN ('pending', 'error', 'waiting_api') LIMIT 1""",
            (uid,),
        ).fetchone()
        if local and pendiente:
            return None
        fila = connection.execute(
            "SELECT * FROM lista_negra WHERE uid = ?",
            (uid,),
        ).fetchone()

    if fila is None:
        return None

    return {
        "id": None,
        "uid": uid,
        "saldo": 0,
        "vigencia": None,
        "tipo_tarjeta_id": None,
        "tipo_tarjeta": "Desconocido",
        "en_lista_negra": 1,
        "motivo_baja": fila["motivo"],
        "fecha_baja": fila["fecha_baja"],
        "pasajero_id": None,
        "nombre_pasajero": "",
    }
