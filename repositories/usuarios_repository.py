import mysql.connector
from database import get_db_connection

def crear_usuario(nombre, email):
    try:
        conn = get_db_connection()
        if not conn: return {"error": "DB Connection failed", "code": 500}
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (Nombre, Email) VALUES (%s, %s)",
            (nombre, email)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return {"id": nuevo_id, "code": 201}

    except mysql.connector.Error as err:
        if err.errno == 1062:          
            return {"error": "El email ya está registrado", "code": 409}
        return {"error": str(err), "code": 500}

def listar_usuarios(limit, offset):
    conn = get_db_connection()
    if not conn: return None, 0
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    conteo_total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT * FROM usuarios LIMIT %s OFFSET %s",
        (limit, offset)
    )
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados, conteo_total

def obtener_usuario(id):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE ID = %s", (id,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado

def actualizar_usuario(id, nombre, email):
    try:
        conn = get_db_connection()
        if not conn: return {"code": 500}
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE usuarios SET Nombre = %s, Email = %s WHERE ID = %s",
            (nombre, email, id)
        )
        filas = cursor.rowcount
        conn.commit()

        cursor.close()
        conn.close()

        if filas == 0:
            return {"code": 404}

        return {"code": 204}

    except mysql.connector.Error as err:
        if err.errno == 1062:
            return {"error": "El email ya está en uso por otro usuario", "code": 409}
        return {"error": str(err), "code": 500}

def borrar_usuario(id):
    conn = get_db_connection()
    if not conn: return 0
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE ID = %s", (id,))
    conn.commit()
    filas = cursor.rowcount

    cursor.close()
    conn.close()

    return filas
