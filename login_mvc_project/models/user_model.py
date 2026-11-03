from core.database import get_connection
from core.seguridad import verificar_password


class UserModel:
    def user_exists(self, username: str) -> bool:
        username = (username or "").strip()

        if not username:
            return False

        with get_connection() as connection:
            usuario = connection.execute(
                """
                SELECT 1 FROM usuarios
                WHERE username = ?
                LIMIT 1
                """,
                (username,),
            ).fetchone()

        return usuario is not None

    def password_matches(
        self,
        username: str,
        password: str,
    ) -> bool:
        username = (username or "").strip()

        if not username or not password:
            return False

        with get_connection() as connection:
            usuario = connection.execute(
                """
                SELECT password FROM usuarios
                WHERE username = ?
                LIMIT 1
                """,
                (username,),
            ).fetchone()

        return bool(
            usuario
            and verificar_password(
                password,
                usuario["password"],
            )
        )

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> tuple[bool, str]:
        if not (username or "").strip() or not password:
            return False, "Debes capturar usuario y contraseña."

        if self.password_matches(username, password):
            return True, "Login correcto."

        return False, "Usuario o contraseña incorrectos."

    def get_role(self, username: str) -> str | None:
        username = (username or "").strip()

        if not username:
            return None

        with get_connection() as connection:
            fila = connection.execute(
                """
                SELECT r.nombre
                FROM usuarios u
                JOIN roles r ON r.id = u.role_id
                WHERE u.username = ?
                LIMIT 1
                """,
                (username,),
            ).fetchone()

        return fila[0] if fila else None