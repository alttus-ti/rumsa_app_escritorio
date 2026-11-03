import sqlite3
from pathlib import Path

from core.seguridad import migrar_passwords


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATABASE_DIR / "matehuala.db"
INIT_SCRIPT_PATH = PROJECT_ROOT / "sqlite_init.sql"


class LocalConnection(sqlite3.Connection):
    """Confirma o revierte la transacción y libera el archivo al salir de with."""

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH, timeout=30, factory=LocalConnection)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 30000")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    DATABASE_DIR.mkdir(exist_ok=True)

    if not INIT_SCRIPT_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el SQL: {INIT_SCRIPT_PATH}"
        )

    script = INIT_SCRIPT_PATH.read_text(encoding="utf-8")

    try:
        with get_connection() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute(
                "PRAGMA journal_size_limit = 2097152"
            )

            existe_pasajeros = connection.execute(
                """
                SELECT 1 FROM sqlite_master
                WHERE type = 'table' AND name = 'pasajeros'
                """
            ).fetchone()

            if existe_pasajeros:
                _ensure_pasajeros_columns(connection)

            connection.executescript(script)
            _ensure_pasajeros_columns(connection)
            _ensure_recargas_columns(connection)
            migrar_passwords(connection)

        from core.operadores_local import migrar_operadores

        migrar_operadores()

        with get_connection() as connection:
            for tabla in ("recargas", "sustituciones"):
                columnas = {
                    fila["name"]
                    for fila in connection.execute(
                        f"PRAGMA table_info({tabla})"
                    )
                }

                nuevas = (
                    ("sync_uuid", "TEXT"),
                    (
                        "sincronizada",
                        "INTEGER NOT NULL DEFAULT 0",
                    ),
                    ("synced_at", "TEXT"),
                )

                for nombre, tipo in nuevas:
                    if nombre not in columnas:
                        connection.execute(
                            f"ALTER TABLE {tabla} "
                            f"ADD COLUMN {nombre} {tipo}"
                        )

        from core.despachadores_local import migrar_despachadores

        migrar_despachadores()

    except sqlite3.OperationalError as error:
        if "database is locked" in str(error).lower():
            raise RuntimeError(
                "La base está bloqueada. Cierra otras ventanas "
                "de la app o DB Browser for SQLite."
            ) from error
        raise


def _ensure_pasajeros_columns(connection):
    columnas = {
        fila["name"]
        for fila in connection.execute(
            "PRAGMA table_info(pasajeros)"
        )
    }

    for nombre in ("curp", "foto", "fecha_nacimiento"):
        if nombre not in columnas:
            connection.execute(
                f"ALTER TABLE pasajeros ADD COLUMN {nombre} TEXT"
            )


def _ensure_recargas_columns(connection):
    columnas = {
        fila["name"]
        for fila in connection.execute(
            "PRAGMA table_info(recargas)"
        )
    }

    if "oficina" not in columnas:
        connection.execute(
            "ALTER TABLE recargas ADD COLUMN oficina TEXT"
        )
