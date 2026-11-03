"""Separación local de DE, sin reconstruir tarjetas ni la base de trabajo."""
import json

from core import database


def migrar_despachadores():
    with database.get_connection() as c:
        c.execute("BEGIN IMMEDIATE")
        c.execute("""
            CREATE TABLE IF NOT EXISTS despachadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarjeta_id INTEGER NOT NULL UNIQUE REFERENCES tarjetas(id),
                nombre TEXT NOT NULL,
                documento TEXT NOT NULL DEFAULT '-',
                curp TEXT,
                foto TEXT,
                fecha_nacimiento TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        filas = c.execute("""
            SELECT o.* FROM operadores o
            JOIN tarjetas t ON t.id = o.tarjeta_id
            JOIN tipo_tarjetas tt ON tt.id = t.tipo_tarjeta_id
            WHERE LOWER(TRIM(tt.clave)) IN ('de', 'despachador')
               OR (LOWER(tt.descripcion) LIKE '%despachador%'
                   AND LOWER(TRIM(tt.clave)) NOT IN ('ki', 'ope', 'operador'))
        """).fetchall()
        campos = ('id', 'tarjeta_id', 'nombre', 'documento', 'curp',
                  'foto', 'fecha_nacimiento', 'created_at')
        for fila in filas:
            existente = c.execute(
                "SELECT * FROM despachadores WHERE tarjeta_id = ?", (fila['tarjeta_id'],)
            ).fetchone()
            datos = tuple(fila[k] for k in campos)
            if existente:
                if tuple(existente[k] for k in campos) != datos:
                    raise RuntimeError(
                        "Hay datos distintos para la misma tarjeta en operadores y "
                        "despachadores. La migración se revirtió para conservarlos."
                    )
            else:
                c.execute("""
                    INSERT INTO despachadores (
                        id, tarjeta_id, nombre, documento, curp,
                        foto, fecha_nacimiento, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, datos)
            c.execute("DELETE FROM operadores WHERE id = ?", (fila['id'],))

        c.execute("DROP VIEW IF EXISTS v_tarjetas_locales")
        c.execute("""
            CREATE VIEW v_tarjetas_locales AS
            SELECT t.*, tt.descripcion AS tipo_tarjeta,
                COALESCE(d.nombre, o.nombre, p.nombre, '') AS nombre_pasajero,
                COALESCE(d.curp, o.curp, p.curp, '') AS curp,
                COALESCE(d.foto, o.foto, p.foto, '') AS foto,
                COALESCE(d.fecha_nacimiento, o.fecha_nacimiento,
                         p.fecha_nacimiento, '') AS fecha_nacimiento,
                COALESCE(d.documento, o.documento, p.documento, '-') AS documento,
                CASE WHEN d.id IS NOT NULL THEN 'despachador'
                     WHEN o.id IS NOT NULL THEN 'operador'
                     ELSE 'pasajero' END AS entidad
            FROM tarjetas t
            JOIN tipo_tarjetas tt ON tt.id = t.tipo_tarjeta_id
            LEFT JOIN pasajeros p ON p.id = t.pasajero_id
            LEFT JOIN operadores o ON o.tarjeta_id = t.id
            LEFT JOIN despachadores d ON d.tarjeta_id = t.id
        """)

        uids_de = {
            str(fila[0]).strip().upper() for fila in c.execute("""
                SELECT t.uid FROM tarjetas t
                JOIN tipo_tarjetas tt ON tt.id = t.tipo_tarjeta_id
                WHERE LOWER(TRIM(tt.clave)) IN ('de', 'despachador')
                   OR (LOWER(tt.descripcion) LIKE '%despachador%'
                       AND LOWER(TRIM(tt.clave)) NOT IN ('ki', 'ope', 'operador'))
            """)
        }
        pendientes = c.execute("""
            SELECT id, entity_uid, payload_json FROM sync_queue
            WHERE status IN ('pending', 'error', 'waiting_api')
        """).fetchall()
        for fila in pendientes:
            payload = json.loads(fila['payload_json'])
            if not isinstance(payload, dict):
                raise ValueError(f"Evento {fila['id']} con payload inválido; migración revertida.")
            original = payload.get('datos_original')
            original = original if isinstance(original, dict) else {}
            tipos = [payload.get('tipo_codigo_local'), payload.get('tipo_tarjeta'),
                     original.get('tipo_codigo_local'), original.get('tipo_tarjeta')]
            uids = [fila['entity_uid'], payload.get('uid'), payload.get('uid_anterior'),
                    payload.get('uid_nueva')]
            es_de = (
                any(str(t or '').strip().lower() == 'de'
                    or 'despachador' in str(t or '').lower() for t in tipos)
                or payload.get('entidad') == 'despachador'
                or any(str(uid or '').strip().upper() in uids_de for uid in uids)
            )
            if es_de:
                corregido = dict(payload, tipo_codigo_local='DE', entidad='despachador')
                if original.get('entidad') == 'operador':
                    corregido['datos_original'] = dict(original, entidad='despachador')
                if corregido != payload:
                    c.execute("UPDATE sync_queue SET payload_json = ? WHERE id = ?",
                              (json.dumps(corregido, ensure_ascii=False), fila['id']))
        if c.execute("PRAGMA foreign_key_check").fetchone():
            raise RuntimeError("Relaciones inválidas; la separación de despachadores se revirtió.")
        c.execute("""
            INSERT OR IGNORE INTO local_migrations(nombre)
            VALUES ('despachadores_separados_v1')
        """)
