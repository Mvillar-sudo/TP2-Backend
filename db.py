import mysql.connector

db_config = {
    'host': "localhost",
    'user': "root",
    'password': "1234",
    'database': "mundial_fixture"
}

def obtener_partidos_paginados(limit, offset):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM partidos ORDER BY fecha LIMIT %s OFFSET %s", (limit, offset))

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
        SET goles_local = %s, goles_visitante = %s
        WHERE id = %s
    """, (goles_local, goles_visitante, id))

    filas_afectadas = cursor.rowcount  # 0 si el ID no existe
    conn.commit()
    cursor.close()
    conn.close()

    return filas_afectadas


def obtener_partido(id): 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM partidos WHERE id = %s", (id,)) 

    resultado = cursor.fetchone() 

    cursor.close()
    conn.close()

    return resultado 

def borrar_partido(id): 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True) 

    cursor.execute("DELETE FROM partidos WHERE id = %s", (id,))

    conn.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conn.close()

    return filas_afectadas
def agregar_prediccion(id, usuario_id, goles_local, goles_visitante):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Verificar que el partido exista
        cursor.execute(
            "SELECT goles_local, goles_visitante FROM partidos WHERE id = %s",
            (id,)
        )
        partido = cursor.fetchone()
        
        if not partido:
            return {'error': 'El partido no existe', 'code': 404}
        
        # Verificar que no esté jugado
        if partido[0] is not None or partido[1] is not None:
            return {'error': 'El partido ya se jugó', 'code': 409}
        
        # Insertar predicción
        cursor.execute("""
            INSERT INTO predicciones (usuario_id, partido_id, goles_local, goles_visitante)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, id, goles_local, goles_visitante))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {'message': 'Predicción registrada', 'code': 201}
    
    except mysql.connector.Error as err:
        # Manejo de duplicado (por UNIQUE)
        if err.errno == 1062:
            return {'error': 'Ya hiciste una predicción para este partido', 'code': 409}
        return {'error': str(err), 'code': 500}