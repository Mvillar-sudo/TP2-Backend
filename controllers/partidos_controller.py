from flask import Blueprint, request, jsonify, url_for
from services import partidos_service

partidos_bp = Blueprint('partidos', __name__, url_prefix='/partidos')

@partidos_bp.route("", methods=['GET'])
def obtener_partidos():
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)
    
    filtros = {k: v for k, v in request.args.items() if k not in ['limit', 'offset']} 

    resultados, conteo_total = partidos_service.obtener_partidos_paginados(limit, offset, filtros) 

    def generar_url_con_filtros(nuevo_offset):
        params = {**filtros, "limit": limit, "offset": nuevo_offset, "_external": True}
        return url_for("partidos.obtener_partidos", **params)
    
    links = {
        "_self": generar_url_con_filtros(offset),
        "_first": generar_url_con_filtros(0),
    }

    if offset + limit < conteo_total:
        links['_next'] = generar_url_con_filtros(offset+limit)

    if offset > 0: 
        offset_previo = max(0, offset - limit)
        links['_prev'] = generar_url_con_filtros(offset_previo)

    if conteo_total > 0:
        ultimo_offset = ((conteo_total - 1) // limit) * limit
    else:
        ultimo_offset = 0
    links['_last'] = generar_url_con_filtros(ultimo_offset)

    return jsonify({
        "data": resultados,
        "total": conteo_total, 
        "links": links
    })

@partidos_bp.route("", methods=["POST"])
def registrar_encuentro():
    datos = request.get_json()

    if not datos:
        return jsonify({'error': "No se enviaron datos"}), 400

    equipo_local = datos.get('Equipo_local')
    equipo_visitante = datos.get('Equipo_visitante')
    fecha = datos.get('Fecha')
    fase = datos.get('Fase')

    if not equipo_local or not equipo_visitante or not fecha or not fase:
         return jsonify({'error': "Falta completar"}), 400

    if equipo_local == equipo_visitante:
        return jsonify({'error': "Los equipos no deben ser iguales"}), 400

    partidos_service.registrar_encuentro(equipo_local, equipo_visitante, fecha, fase)
    return jsonify({'mensaje': "partido creado correctamente"}), 201

@partidos_bp.route("/<int:id>/resultado", methods=["PUT"])
def actualizar_resultado(id):
    datos = request.get_json()

    if not datos:
        return jsonify({"errors": [{"code": "400", "message": "No se enviaron datos", "level": "error"}]}), 400

    goles_local = datos.get("Goles_local")
    goles_visitante = datos.get("Goles_visitante")

    if goles_local is None or goles_visitante is None:
        return jsonify({"errors": [{"code": "400", "message": "Se requieren Goles_local y Goles_visitante", "level": "error"}]}), 400

    if type(goles_local) != int or type(goles_visitante) != int:
        return jsonify({"errors": [{"code": "400", "message": "Los goles deben ser enteros", "level": "error"}]}), 400

    if goles_local < 0 or goles_visitante < 0:
        return jsonify({"errors": [{"code": "400", "message": "Los goles no pueden ser negativos", "level": "error"}]}), 400

    filas = partidos_service.actualizar_resultado(id, goles_local, goles_visitante)

    if filas == 0:
        return jsonify({"errors": [{"code": "404", "message": f"No existe partido con ID {id}", "level": "error"}]}), 404

    return '', 204 

@partidos_bp.route("/<int:id>", methods=['GET']) 
def obtener_partido(id): 
    resultado = partidos_service.obtener_partido(id) 

    if not resultado: 
        return jsonify({"errors": [{"code": "404", "message": f"No existe partido con ID {id}", "level": "error"}]}), 404
    
    return jsonify(resultado), 200

@partidos_bp.route("/<int:id>", methods=['DELETE'])
def borrar_partido(id): 
    fila = partidos_service.borrar_partido(id) 

    if fila == 0: 
        return jsonify({"errors": [{"code": "404", "message": f"No existe partido con ID {id}", "level": "error"}]}), 404
    return '', 204

@partidos_bp.route('/<int:id>/prediccion', methods=['POST'])
def agregar_prediccion(id):
    data = request.get_json()
    
    usuario_id = data.get('id_usuario')
    goles_local = data.get('local')
    goles_visitante = data.get('visitante')
    
    if usuario_id is None or goles_local is None or goles_visitante is None:
        return jsonify({'error': 'Faltan datos'}), 400
    
    result = partidos_service.agregar_prediccion(id, usuario_id, goles_local, goles_visitante)
    return jsonify(result), result.get('code', 201)
