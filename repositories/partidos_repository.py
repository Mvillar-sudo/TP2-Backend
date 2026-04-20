import mysql.connector
from database import get_db_connection

def obtener_partidos_paginados(limit, offset, filtros=None):
    conn = get_db_connection()
    if not conn: return None, 0
    cursor = conn.cursor(dictionary=True) 

    columnas_validas = ['Fecha', 'Fase'] 
    condiciones = []
    valores_sql = []

    if filtros:
        if 'equipo' in filtros and filtros['equipo']:
            nombre_equipo = filtros['equipo']
            condiciones.append("(Equipo_local = %s OR Equipo_visitante = %s)")
            valores_sql.extend([nombre_equipo, nombre_equipo])

        for columna, valor in filtros.items():
            if columna in columnas_validas and valor:
                condiciones.append(f"{columna} = %s")
                valores_sql.append(valor)

    where_condicion = f" WHERE {' AND '.join(condiciones)}" if condiciones else ""

    cursor.execute(f"SELECT COUNT(*) as total FROM partidos{where_condicion}", valores_sql)
    conteo_total = cursor.fetchone()['total']
    
    sql_final = f"SELECT * FROM partidos{where_condicion} ORDER BY Fecha LIMIT %s OFFSET %s"
    cursor.execute(sql_final, valores_sql + [limit, offset])

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados, conteo_total

def registrar_encuentro(Equipo_local, Equipo_visitante, Fecha, Fase):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO partidos (Equipo_local, Equipo_visitante, Fecha, Fase)
                   VALUES (%s, %s, %s, %s)
                   """, (Equipo_local, Equipo_visitante, Fecha, Fase))

    conn.commit()
    cursor.close()
    conn.close()

def actualizar_resultado(id, goles_local, goles_visitante):
    conn = get_db_connection()
    if not conn: return 0
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE partidos
        SET Goles_local = %s, Goles_visitante = %s
        WHERE ID = %s
    """, (goles_local, goles_visitante, id))

    filas_afectadas = cursor.rowcount  
    conn.commit()
    cursor.close()
    conn.close()

    return filas_afectadas

def obtener_partido(id): 
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM partidos WHERE ID = %s", (id,)) 
    resultado = cursor.fetchone() 

    cursor.close()
    conn.close()

    return resultado 

def borrar_partido(id): 
    conn = get_db_connection()
    if not conn: return 0
    cursor = conn.cursor() 

    cursor.execute("DELETE FROM partidos WHERE ID = %s", (id,))
    conn.commit()
    filas_afectadas = cursor.rowcount

    cursor.close()
    conn.close()

    return filas_afectadas

def agregar_prediccion(id, usuario_id, goles_local, goles_visitante):
    try:
        conn = get_db_connection()
        if not conn: return {'error': 'Database connection failed', 'code': 500}
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT Goles_local, Goles_visitante FROM partidos WHERE ID = %s",
            (id,)
        )
        partido = cursor.fetchone()
        
        if not partido:
            return {'error': 'El partido no existe', 'code': 404}
        
        if partido[0] is not None or partido[1] is not None:
            return {'error': 'El partido ya se jugó', 'code': 409}
        
        cursor.execute("""
            INSERT INTO predicciones (id_usuario, id_partido, local, visitante)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, id, goles_local, goles_visitante))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {'message': 'Predicción registrada', 'code': 201}
    
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return {'error': 'Ya hiciste una predicción para este partido', 'code': 409}
        return {'error': str(err), 'code': 500}
