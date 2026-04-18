import mysql.connector

db_config = {
    'host': "localhost",
    'user': "root",
    'password': "1234",
    'database': "mundial_fixture"
}

def obtener_partidos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM partidos")

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados


def registrar_encuentro(Equipo_local, Equipo_visitante, Fecha, Fase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO partidos (Equipo_local, Equipo_visitante, Fecha, Fase)
                   VALUES (%s, %s, %s, %s)
                   """, (Equipo_local, Equipo_visitante, Fecha, Fase))

    conn.commit()
    cursor.close()
    conn.close()

def actualizar_resultado(id, goles_local, goles_visitante):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE partidos
        SET Goles_local = %s, Goles_visitante = %s
        WHERE ID = %s
    """, (goles_local, goles_visitante, id))

    filas_afectadas = cursor.rowcount  # 0 si el ID no existe
    conn.commit()
    cursor.close()
    conn.close()

    return filas_afectadas
