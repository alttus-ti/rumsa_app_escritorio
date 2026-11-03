import re

from core import database


OPERADORES_SQL = """
CREATE TABLE operadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarjeta_id INTEGER NOT NULL UNIQUE REFERENCES tarjetas(id),
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL DEFAULT '-',
    curp TEXT,
    foto TEXT,
    fecha_nacimiento TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
)
"""


def migrar_operadores():
    c = database.get_connection()

    try:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS local_migrations (
                nombre TEXT PRIMARY KEY
            )
            """
        )
        c.commit()

        if c.execute(
            """
            SELECT 1 FROM local_migrations
            WHERE nombre = 'operadores_separados_v1'
            """
        ).fetchone():
            return

        c.execute("PRAGMA foreign_keys = OFF")
        c.execute("BEGIN IMMEDIATE")
        c.execute(
            "DROP TRIGGER IF EXISTS actualizar_datos_operador"
        )
        c.execute("DROP VIEW IF EXISTS v_tarjetas_locales")

        columnas = list(c.execute("PRAGMA table_info(tarjetas)"))

        if any(
            fila["name"] == "pasajero_id" and fila["notnull"]
            for fila in columnas
        ):
            sql = c.execute(
                """
                SELECT sql FROM sqlite_master
                WHERE type = 'table' AND name = 'tarjetas'
                """
            ).fetchone()[0]

            sql = re.sub(
                r'CREATE TABLE\s+(?:IF NOT EXISTS\s+)?["`\[]?tarjetas["`\]]?',
                "CREATE TABLE tarjetas_nueva",
                sql,
                count=1,
                flags=re.I,
            )

            sql = re.sub(
                r"(pasajero_id\s+INTEGER)\s+NOT\s+NULL",
                r"\1",
                sql,
                flags=re.I,
            )

            indices = [
                fila[0]
                for fila in c.execute(
                    """
                    SELECT sql FROM sqlite_master
                    WHERE type = 'index'
                      AND tbl_name = 'tarjetas'
                      AND sql IS NOT NULL
                    """
                )
            ]

            c.execute(sql)

            nombres = ",".join(
                '"' + fila["name"] + '"' for fila in columnas
            )

            c.execute(
                f"INSERT INTO tarjetas_nueva ({nombres}) "
                f"SELECT {nombres} FROM tarjetas"
            )

            c.execute("DROP TABLE tarjetas")
            c.execute(
                "ALTER TABLE tarjetas_nueva RENAME TO tarjetas"
            )

            for sql_indice in indices:
                c.execute(sql_indice)

        anteriores = [
            dict(fila)
            for fila in c.execute("SELECT * FROM operadores")
        ]

        c.execute("DROP TABLE operadores")
        c.execute(OPERADORES_SQL)

        for operador in anteriores:
            tarjeta = c.execute(
                "SELECT * FROM tarjetas WHERE id = ?",
                (operador.get("tarjeta_id"),),
            ).fetchone()

            pasajero_id = operador.get("pasajero_id")

            if not pasajero_id and tarjeta:
                pasajero_id = tarjeta["pasajero_id"]

            pasajero = c.execute(
                "SELECT * FROM pasajeros WHERE id = ?",
                (pasajero_id,),
            ).fetchone()

            datos = dict(pasajero) if pasajero else {}
            datos.update({
                clave: valor
                for clave, valor in operador.items()
                if valor is not None
            })

            c.execute(
                """
                INSERT INTO operadores (
                    id, tarjeta_id, nombre, documento,
                    curp, foto, fecha_nacimiento, created_at
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?,
                    COALESCE(?, datetime('now'))
                )
                """,
                (
                    operador["id"],
                    operador["tarjeta_id"],
                    datos.get("nombre") or "Operador",
                    datos.get("documento") or "-",
                    datos.get("curp"),
                    datos.get("foto"),
                    datos.get("fecha_nacimiento"),
                    datos.get("created_at"),
                ),
            )

        tarjetas = c.execute(
            """
            SELECT
                t.*,
                p.nombre,
                p.documento,
                p.curp,
                p.foto,
                p.fecha_nacimiento,
                p.created_at AS persona_created_at
            FROM tarjetas t
            JOIN tipo_tarjetas tt ON tt.id = t.tipo_tarjeta_id
            LEFT JOIN pasajeros p ON p.id = t.pasajero_id
            WHERE (
                LOWER(tt.clave) IN ('operador', 'ki', 'ope')
                OR LOWER(tt.descripcion) LIKE '%operador%'
            )
            OR EXISTS (
                SELECT 1 FROM operadores o
                WHERE o.tarjeta_id = t.id
            )
            """
        ).fetchall()

        pasajeros_a_revisar = set()

        for tarjeta in tarjetas:
            c.execute(
                """
                INSERT INTO operadores (
                    tarjeta_id, nombre, documento,
                    curp, foto, fecha_nacimiento, created_at
                )
                SELECT
                    ?, ?, ?, ?, ?, ?,
                    COALESCE(?, datetime('now'))
                WHERE NOT EXISTS (
                    SELECT 1 FROM operadores WHERE tarjeta_id = ?
                )
                """,
                (
                    tarjeta["id"],
                    tarjeta["nombre"] or "Operador",
                    tarjeta["documento"] or "-",
                    tarjeta["curp"],
                    tarjeta["foto"],
                    tarjeta["fecha_nacimiento"],
                    tarjeta["persona_created_at"],
                    tarjeta["id"],
                ),
            )

            if tarjeta["pasajero_id"] is not None:
                pasajeros_a_revisar.add(tarjeta["pasajero_id"])

            c.execute(
                "UPDATE tarjetas SET pasajero_id = NULL WHERE id = ?",
                (tarjeta["id"],),
            )

        for pasajero_id in pasajeros_a_revisar:
            c.execute(
                """
                DELETE FROM pasajeros
                WHERE id = ?
                  AND NOT EXISTS (
                      SELECT 1 FROM tarjetas WHERE pasajero_id = ?
                  )
                """,
                (pasajero_id, pasajero_id),
            )

        c.execute(
            """
            CREATE VIEW v_tarjetas_locales AS
            SELECT
                t.*,
                tt.descripcion AS tipo_tarjeta,
                COALESCE(o.nombre, p.nombre, '') AS nombre_pasajero,
                COALESCE(o.curp, p.curp, '') AS curp,
                COALESCE(o.foto, p.foto, '') AS foto,
                COALESCE(
                    o.fecha_nacimiento,
                    p.fecha_nacimiento,
                    ''
                ) AS fecha_nacimiento,
                COALESCE(o.documento, p.documento, '-') AS documento,
                CASE
                    WHEN o.id IS NOT NULL THEN 'operador'
                    ELSE 'pasajero'
                END AS entidad
            FROM tarjetas t
            JOIN tipo_tarjetas tt ON tt.id = t.tipo_tarjeta_id
            LEFT JOIN pasajeros p ON p.id = t.pasajero_id
            LEFT JOIN operadores o ON o.tarjeta_id = t.id
            """
        )

        c.execute(
            """
            INSERT INTO local_migrations(nombre)
            VALUES ('operadores_separados_v1')
            """
        )

        if list(c.execute("PRAGMA foreign_key_check")):
            raise RuntimeError(
                "La migración detectó relaciones inválidas "
                "y no se aplicó."
            )

        c.commit()

    except Exception:
        c.rollback()
        raise

    finally:
        c.execute("PRAGMA foreign_keys = ON")
        c.close()
