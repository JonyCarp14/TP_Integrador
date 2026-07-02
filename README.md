# CRUD Flask + PostgreSQL

Trabajo práctico intermedio: aplicación web para gestionar estudiantes con Flask y PostgreSQL.

## 1. Crear entorno virtual

```bash
python -m venv venv
```

Activar en Windows:

```bash
venv\Scripts\activate
```

Activar en Linux/Mac:

```bash
source venv/bin/activate
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Crear base de datos

Entrar a PostgreSQL y ejecutar el archivo:

```bash
psql -U postgres -f database.sql
```

Si la base ya existe, crear solo la tabla conectándose a `flask_crud`.

## 4. Configurar variables de entorno

Copiar `.env.example` como `.env` y modificar usuario/clave si corresponde:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flask_crud
DB_USER=postgres
DB_PASSWORD=postgres
```

## 5. Ejecutar la aplicación

```bash
python app.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Funcionalidades

- Listar estudiantes.
- Agregar estudiante.
- Editar estudiante.
- Eliminar estudiante.
- Buscar por DNI, apellido o nombre.
