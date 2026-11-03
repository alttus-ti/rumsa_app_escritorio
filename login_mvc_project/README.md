# Login MVC con flujo tipo AppController

Este proyecto ahora usa una estructura parecida al `urban_aeropuerto_app`:

- `AppController` controla que ventana se muestra.
- `LoginWindow` maneja la UI del login y valida credenciales.
- `LoginController` contiene la logica de autenticacion.
- `ContadorWindow` es la pantalla que abre despues de iniciar sesion.
- `AppController` incluye metodos estilo referencia: `showLoginWindow()` y `showContadorWindow()`.

## Estructura

```text
login_mvc_project/
|-- main.py
|-- controllers/
|   |-- app_controller.py
|   |-- auth_controller.py
|   |-- login_controller.py
|   `-- route_controller.py
|-- models/
|   `-- user_model.py
|-- views/
|   |-- login_view.py
|   `-- contador_view.py
|-- core/
|   `-- ui_loader.py
`-- ui/
    |-- login_qtdesigner.ui
    `-- contador.ui
```

## Ejecucion

Instala las dependencias con el mismo intérprete que utilizarás para abrir la app:

```powershell
python -m pip install -r requirements.txt
```

```powershell
python main.py
```

Al iniciar, la app crea automaticamente la base local desde `sqlite_init.sql` en:

```text
data/matehuala.db
```

La carpeta `data/` no se sube al repositorio porque contiene la base generada en cada equipo.

Usuario de prueba:

- Usuario: `admin`
- Contrasena: `1234`

## Uso de SQLite

La conexion esta centralizada en `core/database.py`:

- `initialize_database()` crea la base y ejecuta `sqlite_init.sql`.
- `get_connection()` abre una conexion con `PRAGMA foreign_keys = ON`.

Ejemplo para consultar datos desde un modelo:

```python
from core.database import get_connection

with get_connection() as connection:
    usuarios = connection.execute("SELECT * FROM usuarios").fetchall()
```

Al salir del bloque `with`, la conexión confirma los cambios (o los revierte si
hay un error) y se cierra. Si abres una conexión sin `with`, debes cerrarla.

## Tarjetas y operación sin conexión

El administrador tiene opciones para pasajeros y operadores. Las tarjetas de
pasajeros usan los códigos `NO` (normal) y `EU` (preferencial); las de operadores
usan `KI`. Los operadores se guardan en su propia tabla y no admiten recargas.
Ambos pueden usar las pantallas de sustitución y cancelación.

Las operaciones se guardan en SQLite junto con sus eventos en `sync_queue`.
La sincronización se ejecuta en segundo plano cuando hay conexión; los eventos
pendientes permanecen en el equipo hasta recibir confirmación del servidor.
La configuración se encuentra en `core/sync_config.py`.

Al iniciar también se aplican las migraciones locales y la conversión de
contraseñas antiguas a hashes. Conserva la carpeta `data/` entre ejecuciones.

## Validación sin hardware

```powershell
python -m unittest test_offline -v
```

Estas pruebas usan una base temporal y respuestas HTTP simuladas. No modifican
la base de trabajo ni requieren conectar el lector Arduino.
