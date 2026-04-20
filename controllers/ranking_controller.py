from flask import Blueprint, request, jsonify
from services.ranking_service import get_ranking_service

ranking_bp = Blueprint('ranking_bp', __name__)

@ranking_bp.route('/ranking', methods=['GET'])
def get_ranking():
    try:
        # Extraemos los parámetros de paginación que envía el frontend en la URL
        # Si no los envía, por defecto limit será 10 y offset 0
        limit = int(request.args.get("_limit", 10))
        offset = int(request.args.get("_offset", 0))
    except ValueError:
        # Si el Frontend o el usuario envían texto en lugar de números en la URL (ej: ?_limit=diez)
        # Se captura el error y se devuelve un 400 Bad Request cumpliendo la estructura de "Errores" del Swagger
        return jsonify({
            "errors": [{
                "code": "BAD_PARAMS",
                "message": "Parámetros inválidos",
                "level": "error",
                "description": "_limit y _offset deben ser enteros numéricos"
            }]
        }), 400

    if limit < 1 or offset < 0:
        # No se pueden pedir páginas de 0 elementos o empezar en un índice negativo
        return jsonify({
            "errors": [{
                "code": "BAD_PARAMS",
                "message": "Valores fuera de rango",
                "level": "error",
                "description": "_limit debe ser >= 1 y _offset >= 0"
            }]
        }), 400

    try:
        ranking_items, total_users = get_ranking_service(limit, offset)
        if not ranking_items:
            return '', 204
    except Exception as e:
        # Catch-all para cualquier error grave (ej: la base de datos está caída)
        # Devuelve un 500 Internal Server Error para no colgar la aplicación entera
        return jsonify({
            "errors": [{
                "code": "SERVER_ERROR",
                "message": "Error interno de base de datos o servidor",
                "level": "error",
                "description": str(e)
            }]
        }), 500

    # Generación de la paginación HATEOAS
    base_url = request.base_url

    next_offset = offset + limit
    prev_offset = max(0, offset - limit)
    
    # Calculamos en qué índice (offset) empieza la última página posible
    if total_users > 0:
        last_offset = max(0, ((total_users - 1) // limit) * limit)
    else:
        last_offset = 0

    _links = {
        "_first": {"href": f"{base_url}?_offset=0&_limit={limit}"},
        "_prev": {"href": f"{base_url}?_offset={prev_offset}&_limit={limit}"},
        "_next": {"href": f"{base_url}?_offset={next_offset}&_limit={limit}"},
        "_last": {"href": f"{base_url}?_offset={last_offset}&_limit={limit}"}
    }

    return jsonify({
        "ranking": ranking_items,
        "_links": _links
    }), 200
