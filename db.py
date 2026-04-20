import mysql.connector
db_config = {

    'host': "localhost",
    'user': "root",
    'password': "1234",
    'database': "mundial_fixture"
}

def obtener_partidos_paginados(limit, offset, filtros=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True) 

    columnas_validas = ['Fecha', 'Fase'] 
    condiciones = []
    valores_sql = []

    if filtros:
        # Filtro por Equipo (Local O Visitante)
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
    conteo_total  = cursor.fetchone()['total']
    
    sql_final = f"SELECT * FROM partidos{where_condicion} ORDER BY Fecha LIMIT %s OFFSET %s"
    cursor.execute(sql_final, valores_sql + [limit, offset])

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados, conteo_total


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


def obtener_partido(id): 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM partidos WHERE ID = %s", (id,)) 

    resultado = cursor.fetchone() 

    cursor.close()
    conn.close()

    return resultado 

def borrar_partido(id): 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 

    cursor.execute("DELETE FROM partidos WHERE ID = %s", (id,))

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
            "SELECT Goles_local, Goles_visitante FROM partidos WHERE ID = %s",
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
            INSERT INTO predicciones (id_usuario, id_partido, local, visitante)
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


def crear_usuario(nombre, email):
    try:
        conn   = mysql.connector.connect(**db_config)
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
        if err.errno == 1062:          # Email duplicado (UNIQUE)
            return {"error": "El email ya está registrado", "code": 409}
        return {"error": str(err), "code": 500}


def listar_usuarios(limit, offset):
    conn   = mysql.connector.connect(**db_config)
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
    conn   = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE ID = %s", (id,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado


def actualizar_usuario(id, nombre, email):
    try:
        conn   = mysql.connector.connect(**db_config)
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
    conn   = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE ID = %s", (id,))
    conn.commit()
    filas = cursor.rowcount

    cursor.close()
    conn.close()

    return filas