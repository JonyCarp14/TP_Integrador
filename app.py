import os
import psycopg2
import re
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

load_dotenv()

app = Flask(__name__)
app.secret_key = "clave_secreta_para_mensajes"


def get_connection():
    """Crea una conexión a PostgreSQL usando variables de entorno."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "flask_crud"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgre"),
        cursor_factory=RealDictCursor,
    )


@app.route("/")
def index():
    # Capturamos el criterio de ordenamiento de la URL, por defecto ordena por id
    orden_por = request.args.get('orden', 'id')
    
    # Validamos que solo acepte columnas permitidas para evitar inyección SQL
    columnas_validas = {
        'apellido': 'apellido ASC',
        'carrera': 'carrera ASC',
        'fecha': 'id ASC' # Si no tienes columna fecha_registro, usamos 'id' como orden cronológico
    }
    
    criterio = columnas_validas.get(orden_por, 'id ASC')

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM estudiantes ORDER BY {criterio}")
            estudiantes = cur.fetchall()
    return render_template("index.html", estudiantes=estudiantes)



@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        dni = request.form.get("dni", "").strip()
        apellido = request.form.get("apellido", "").strip()
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        carrera = request.form.get("carrera", "").strip()
        # Punto 6: Capturar los nuevos campos
        telefono = request.form.get("telefono", "").strip()
        edad = request.form.get("edad", "").strip()

        # Punto 2: Validaciones obligatorias extendidas
        if not dni or not apellido or not nombre or not email:
            flash("DNI, apellido, nombre y email son obligatorios.", "error")
            return redirect(url_for("agregar"))
        
        # Punto 2: Validación de formato de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Por favor, ingrese un email válido.", "error")
            return redirect(url_for("agregar"))

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    # Punto 6: Actualizar el INSERT con teléfono y edad
                    cur.execute(
                        """
                        INSERT INTO estudiantes (dni, apellido, nombre, email, carrera, telefono, edad)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (dni, apellido, nombre, email, carrera, telefono, edad if edad else None),
                    )
                conn.commit()
            flash("Estudiante agregado correctamente.", "success")
            return redirect(url_for("index"))
        except psycopg2.errors.UniqueViolation:
            flash("Ya existe un estudiante con ese DNI.", "error")
            return redirect(url_for("agregar"))
        except Exception as e:
            flash(f"Error al agregar estudiante: {e}", "error")
            return redirect(url_for("agregar"))

    return render_template("agregar.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        dni = request.form.get("dni", "").strip()
        apellido = request.form.get("apellido", "").strip()
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        carrera = request.form.get("carrera", "").strip()
        telefono = request.form.get("telefono", "").strip()
        edad = request.form.get("edad", "").strip()

        if email:
            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_regex, email):
                flash("Email invalido.", "error")
                return redirect(url_for("editar", id=id))
        if not dni or not apellido or not nombre:
            flash("DNI, apellido y nombre son obligatorios.", "error")
            return redirect(url_for("editar", id=id))

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE estudiantes
                        SET dni=%s, apellido=%s, nombre=%s, email=%s, carrera=%s, telefono=%s, edad=%s
                        WHERE id=%s
                        """,
                        (dni, apellido, nombre, email, carrera,telefono, edad, id),
                    )
                conn.commit()
            flash("Estudiante actualizado correctamente.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error al actualizar estudiante: {e}", "error")
            return redirect(url_for("editar", id=id))

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM estudiantes WHERE id = %s", (id,))
            estudiante = cur.fetchone()

    if not estudiante:
        flash("No se encontró el estudiante solicitado.", "error")
        return redirect(url_for("index"))

    return render_template("editar.html", estudiante=estudiante)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM estudiantes WHERE id = %s", (id,))
        conn.commit()
    flash("Estudiante eliminado correctamente.", "success")
    return redirect(url_for("index"))


@app.route("/buscar", methods=["POST"])
def buscar():
    texto = request.form.get("buscar", "").strip()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM estudiantes
                WHERE dni ILIKE %s OR apellido ILIKE %s OR nombre ILIKE %s
                ORDER BY id ASC
                """,
                (f"%{texto}%", f"%{texto}%", f"%{texto}%"),
            )
            estudiantes = cur.fetchall()

    return render_template("index.html", estudiantes=estudiantes, busqueda=texto)


@app.route("/about")
def about():
    # Creamos una lista con las tecnologías para pasarle al HTML
    tecnologias = ["Python", "Flask", "PostgreSQL", "HTML5", "CSS3", "Psycopg2"]
    return render_template("about.html", tecnologias=tecnologias)


if __name__ == "__main__":
    app.run(debug=True)
