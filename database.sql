CREATE DATABASE flask_crud;

-- Conectarse luego a la base flask_crud y ejecutar:

CREATE TABLE IF NOT EXISTS estudiantes (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(15) NOT NULL UNIQUE,
    apellido VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    carrera VARCHAR(120),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO estudiantes (dni, apellido, nombre, email, carrera) VALUES
('30111222', 'Pérez', 'María', 'maria.perez@email.com', 'Tecnicatura en Desarrollo de Software'),
('32222333', 'Gómez', 'Juan', 'juan.gomez@email.com', 'Tecnicatura en Desarrollo de Software'),
('34333444', 'Rodríguez', 'Ana', 'ana.rodriguez@email.com', 'Programación')
ON CONFLICT (dni) DO NOTHING;
ALTER TABLE estudiantes 
ADD COLUMN telefono VARCHAR(20),
ADD COLUMN edad INTEGER;
