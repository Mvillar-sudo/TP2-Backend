from repositories import partidos_repository

def obtener_partidos_paginados(limit, offset, filtros):
    return partidos_repository.obtener_partidos_paginados(limit, offset, filtros)

def registrar_encuentro(equipo_local, equipo_visitante, fecha, fase):
    partidos_repository.registrar_encuentro(equipo_local, equipo_visitante, fecha, fase)

def actualizar_resultado(id, goles_local, goles_visitante):
    return partidos_repository.actualizar_resultado(id, goles_local, goles_visitante)

def obtener_partido(id):
    return partidos_repository.obtener_partido(id)

def borrar_partido(id):
    return partidos_repository.borrar_partido(id)

def agregar_prediccion(id, usuario_id, goles_local, goles_visitante):
    return partidos_repository.agregar_prediccion(id, usuario_id, goles_local, goles_visitante)
