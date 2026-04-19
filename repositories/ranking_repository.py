from database import get_db_connection

def get_ranking_from_db(limit=10, offset=0):
    """
    Consulta a SQLite/MySQL para obtener el ranking ordenado.
    Calcula dinámicamente los puntos base de las predicciones vs. resultados.
    """
    conn = get_db_connection()
    if not conn:
        raise Exception("Error de conexión a la base de datos de MySQL")
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Lógica de la consulta:
        # 1. Partimos de la tabla usuarios (para que aparezcan todos, incluso si no tienen predicciones).
        # 2. Unimos (LEFT JOIN) sus predicciones.
        # 3. Unimos (LEFT JOIN) los partidos correspondientes a esas predicciones.
        # 4. COALESCE asegura que si alguien no tiene puntos, devuelva 0 en lugar de NULL.
        query = """
            SELECT u.id as id_usuario, 
                CAST(COALESCE(SUM(
                    CASE 
                        -- Si el partido aún no se jugó (goles en NULL), no suma puntos.
                        WHEN pa.goles_local IS NULL OR pa.goles_visitante IS NULL THEN 0
                        
                        -- Acierto exacto: mismos goles para ambos equipos -> 3 Puntos
                        WHEN pr.local = pa.goles_local AND pr.visitante = pa.goles_visitante THEN 3
                        
                        -- Acierto parcial -> 1 Punto
                        WHEN SIGN(pr.local - pr.visitante) = SIGN(pa.goles_local - pa.goles_visitante) THEN 1
                        
                        -- Predicción incorrecta -> 0 Puntos
                        ELSE 0 
                    END
                ), 0) AS UNSIGNED) as puntos
            FROM usuarios u
            LEFT JOIN predicciones pr ON u.id = pr.id_usuario
            LEFT JOIN partidos pa ON pr.id_partido = pa.id
            GROUP BY u.id
            ORDER BY puntos DESC, u.id ASC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
        conn.close()

def get_total_users():
    """Obtiene el número total de usuarios para la paginación HATEOAS."""
    conn = get_db_connection()
    if not conn:
        raise Exception("Error de conexión a la base de datos")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM usuarios")
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        conn.close()
