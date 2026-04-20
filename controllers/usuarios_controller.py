from flask import Blueprint, request, jsonify, url_for
from services import usuarios_service

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route("", methods=["POST"])
def crear_usuario():
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se enviaron datos"}), 400

    nombre = datos.get("nombre")
    email  = datos.get("email")

    if not nombre or not email:
        return jsonify({"error": "Se requieren nombre y email"}), 400

    resultado = usuarios_service.crear_usuario(nombre, email)

    if resultado.get("code") == 409:
        return jsonify({"error": resultado["error"]}), 409

    return jsonify({"mensaje": "Usuario creado correctamente", "id": resultado["id"]}), 201

@usuarios_bp.route("", methods=["GET"])
def listar_usuarios():
    limit  = request.args.get("limit",  default=10, type=int)
    offset = request.args.get("offset", default=0,  type=int)

    resultados, conteo_total = usuarios_service.listar_usuarios(limit, offset)

    links = {
        "_self":  url_for("usuarios.listar_usuarios", limit=limit, offset=offset,            _external=True),
        "_first": url_for("usuarios.listar_usuarios", limit=limit, offset=0,                 _external=True),
    }

    if offset + limit < conteo_total:
        links["_next"] = url_for("usuarios.listar_usuarios", limit=limit, offset=offset + limit, _external=True)

    if offset > 0:
        links["_prev"] = url_for("usuarios.listar_usuarios", limit=limit, offset=max(0, offset - limit), _external=True)

    ultimo_offset = (conteo_total // limit) * limit
    if ultimo_offset == conteo_total and conteo_total > 0:
        ultimo_offset -= limit
    links["_last"] = url_for("usuarios.listar_usuarios", limit=limit, offset=ultimo_offset, _external=True)

    return jsonify({"data": resultados, "total": conteo_total, "links": links})

@usuarios_bp.route("/<int:id>", methods=["GET"])
def obtener_usuario(id):
    resultado = usuarios_service.obtener_usuario(id)

    if not resultado:
        return jsonify({"errors": [{"code": "404", "message": f"No existe usuario con ID {id}", "level": "error"}]}), 404

    return jsonify(resultado), 200

@usuarios_bp.route("/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    datos = request.get_json()

    if not datos:
        return jsonify({"errors": [{"code": "400", "message": "No se enviaron datos", "level": "error"}]}), 400

    nombre = datos.get("nombre")
    email  = datos.get("email")

    if not nombre or not email:
        return jsonify({"errors": [{"code": "400", "message": "Se requieren nombre y email", "level": "error"}]}), 400

    resultado = usuarios_service.actualizar_usuario(id, nombre, email)

    if resultado.get("code") == 404:
        return jsonify({"errors": [{"code": "404", "message": f"No existe usuario con ID {id}", "level": "error"}]}), 404

    if resultado.get("code") == 409:
        return jsonify({"errors": [{"code": "409", "message": resultado["error"], "level": "error"}]}), 409

    return "", 204

@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def borrar_usuario(id):
    filas = usuarios_service.borrar_usuario(id)

    if filas == 0:
        return jsonify({"errors": [{"code": "404", "message": f"No existe usuario con ID {id}", "level": "error"}]}), 404

    return "", 204
