CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    fullname TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    access_level TEXT NOT NULL,
    assigned_maintenance_id TEXT
);

CREATE TABLE IF NOT EXISTS maintenance_orders (
    id TEXT PRIMARY KEY,
    supervisor_id TEXT NOT NULL,
    equipment_code TEXT NOT NULL,
    maintenance_date TEXT NOT NULL,
    is_pending INTEGER NOT NULL CHECK (is_pending IN (0, 1)),
    details TEXT,
    -- Referencias a tablas externas
    FOREIGN KEY (supervisor_id) REFERENCES users(id),
    FOREIGN KEY (equipment_code) REFERENCES equipments(id)

);

CREATE TABLE IF NOT EXISTS maintenance_technicians (
    maintenance_id TEXT NOT NULL,
    technician_id TEXT NOT NULL,
    PRIMARY KEY (maintenance_id, technician_id),
    FOREIGN KEY (maintenance_id) REFERENCES maintenance_orders(id),
    FOREIGN KEY (technician_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS equipments (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    provider TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS spare_inventory (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount INTEGER NOT NULL DEFAULT 0
)