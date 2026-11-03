import base64
import hashlib
import hmac
import secrets


ITERACIONES = 600_000
PREFIJO = "pbkdf2_sha256"


def hashear_password(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("La contraseña no puede estar vacía.")

    sal = secrets.token_bytes(16)

    resultado = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        sal,
        ITERACIONES,
    )

    return "$".join((
        PREFIJO,
        str(ITERACIONES),
        base64.b64encode(sal).decode("ascii"),
        base64.b64encode(resultado).decode("ascii"),
    ))


def verificar_password(password: str, guardado: str) -> bool:
    try:
        esquema, rondas, sal_texto, hash_texto = guardado.split("$")
        rondas = int(rondas)

        if esquema != PREFIJO or not 1 <= rondas <= 2_000_000:
            return False

        sal = base64.b64decode(sal_texto, validate=True)
        esperado = base64.b64decode(hash_texto, validate=True)

        if len(sal) < 16 or len(esperado) != 32:
            return False

        calculado = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            sal,
            rondas,
        )

        return hmac.compare_digest(calculado, esperado)

    except (
        ValueError,
        TypeError,
        AttributeError,
        OverflowError,
    ):
        return False


def migrar_passwords(connection):
    usuarios = connection.execute(
        "SELECT id, password FROM usuarios"
    ).fetchall()

    for usuario in usuarios:
        actual = usuario["password"]

        if actual and not actual.startswith(PREFIJO + "$"):
            connection.execute(
                """
                UPDATE usuarios
                SET password = ?
                WHERE id = ? AND password = ?
                """,
                (
                    hashear_password(actual),
                    usuario["id"],
                    actual,
                ),
            )