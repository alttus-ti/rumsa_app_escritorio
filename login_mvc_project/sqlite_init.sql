-- Script de inicialización para SQLite

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS tipo_tarjetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    clave TEXT NOT NULL,
    saldo_maximo REAL NOT NULL DEFAULT 0.00,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS pasajeros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL,
    curp TEXT,
    foto TEXT,
    fecha_nacimiento TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS tarjetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    saldo REAL NOT NULL DEFAULT 0.00,
    tipo_tarjeta_id INTEGER NOT NULL,
    pasajero_id INTEGER,
    vigencia TEXT,
    en_lista_negra INTEGER NOT NULL DEFAULT 0,
    fecha_baja TEXT,
    motivo_baja TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (tipo_tarjeta_id) REFERENCES tipo_tarjetas(id),
    FOREIGN KEY (pasajero_id) REFERENCES pasajeros(id)
);

CREATE TABLE IF NOT EXISTS operadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarjeta_id INTEGER NOT NULL UNIQUE REFERENCES tarjetas(id),
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL DEFAULT '-',
    curp TEXT,
    foto TEXT,
    fecha_nacimiento TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS recargas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarjeta_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    oficina TEXT,
    fecha_hora TEXT NOT NULL DEFAULT (datetime('now')),
    conexion_internet INTEGER NOT NULL DEFAULT 0,
    referencia TEXT,
    sync_uuid TEXT,
    sincronizada INTEGER NOT NULL DEFAULT 0,
    synced_at TEXT,
    FOREIGN KEY (tarjeta_id) REFERENCES tarjetas(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS sustituciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid_anterior TEXT NOT NULL,
    uid_nueva TEXT NOT NULL,
    nueva_vigencia TEXT,
    saldo_transferido REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    sync_uuid TEXT,
    sincronizada INTEGER NOT NULL DEFAULT 0,
    synced_at TEXT
);

CREATE TABLE IF NOT EXISTS sync_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_uuid TEXT NOT NULL UNIQUE,
    event_type TEXT NOT NULL,
    entity_uid TEXT,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    retries INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    synced_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_sync_queue_status_created_at
ON sync_queue(status, created_at);

CREATE TABLE IF NOT EXISTS lista_negra (
    uid TEXT PRIMARY KEY,
    motivo TEXT,
    fecha_baja TEXT
);

CREATE TABLE IF NOT EXISTS blacklist_stage (
    uid TEXT PRIMARY KEY,
    motivo TEXT,
    fecha_baja TEXT
);

CREATE TABLE IF NOT EXISTS local_settings (
    clave TEXT PRIMARY KEY,
    valor TEXT
);

CREATE TABLE IF NOT EXISTS uploaded_photos (
    local_path TEXT PRIMARY KEY,
    remote_path TEXT NOT NULL
);

INSERT OR IGNORE INTO roles(id, nombre, descripcion) VALUES
(1, 'administrador', 'Usuario con permisos completos'),
(2, 'empleado', 'Usuario con permisos de empleado');

INSERT OR IGNORE INTO tipo_tarjetas(
    id, descripcion, clave, saldo_maximo
) VALUES
(1, 'Normal', 'normal', 0.00),
(2, 'Preferencial', 'preferencial', 0.00);

INSERT INTO tipo_tarjetas(
    descripcion, clave, saldo_maximo
)
SELECT 'Operador', 'operador', 0.00
WHERE NOT EXISTS (
    SELECT 1 FROM tipo_tarjetas WHERE clave = 'operador'
);

INSERT INTO tipo_tarjetas (
    descripcion, clave, saldo_maximo
)
SELECT 'Despachador', 'despachador', 0.00
WHERE NOT EXISTS (
    SELECT 1
    FROM tipo_tarjetas
    WHERE clave = 'despachador'
);

INSERT INTO usuarios (username, password, role_id)
SELECT 'admin', '1234', 1
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE username = 'admin'
);

INSERT INTO usuarios (username, password, role_id)
SELECT 'empleado', '1234', 2
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE username = 'empleado'
);