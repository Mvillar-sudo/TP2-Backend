from flask import Flask, request, jsonify, url_for
import db 

app = Flask(__name__)

@app.route("/partidos",methods=['GET'])
def obtener_partidos():
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)
    
    #Lee el URL para encontrar si se pasaron filtros y los convierte en un diccionario: Ej. /partidos?equipo=Brasil&Fase=Grupos
    filtros = {k: v for k, v in request.args.items() if k not in ['limit', 'offset']} 

    resultados, conteo_total = db.obtener_partidos_paginados(limit, offset, filtros) 

    def generar_url_con_filtros(nuevo_offset):
        # Une limit y el nuevo offset con los filtros actuales
        params = {**filtros, "limit": limit, "offset": nuevo_offset, "_external": True}
        return url_for("obtener_partidos", **params)
    
    links = {
        "_self": generar_url_con_filtros(offset),
        "_first": generar_url_con_filtros(0),
    }

    if offset + limit < conteo_total:
        links['_next'] = generar_url_con_filtros(offset+limit)

    if offset > 0: 
        offset_previo = max(0, offset - limit)
        links['_prev'] = generar_url_con_filtros(offset_previo)

    ultimo_offset = (max(0, conteo_total - 1) // limit) * limit
    links['_last'] = generar_url_con_filtros(ultimo_offset)

    return jsonify({
        "data": resultados,
        "total": conteo_total, 
        "links": links
    })



@app.route("/partidos", methods=["POST"])
def registrar_encuentro():

    datos =  request.get_json()

    Equipo_local = datos.get('Equipo_local')
    Equipo_visitante = datos.get('Equipo_visitante')
    Fecha = datos.get('Fecha')
    Fase = datos.get('Fase')


    if not datos:
        return jsonify({'error': "No se enviaron datos"}), 400
    
    elif not datos.get("Equipo_local") or not datos.get("Equipo_visitante") or not datos.get("Fecha") or not datos.get("Fase"):
         return jsonify({'error': "Falta completar"}), 400

    if Equipo_local == Equipo_visitante:
        return jsonify({'error': "Los equipos no deben ser iguales"}), 400

    db.registrar_encuentro(Equipo_local, Equipo_visitante, Fecha, Fase)
    return jsonify({'mensaje': "partido creado correctamente"}), 201

@app.route("/partidos/<int:id>/resultado", methods=["PUT"])
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

    filas = db.actualizar_resultado(id, goles_local, goles_visitante)

    if filas == 0:
        return jsonify({"errors": [{"code": "404", "message": f"No existe partido con ID {id}", "level": "error"}]}), 404

    return '', 204 

@app.route("/partidos/<int:id>", methods=['GET']) 
def obtener_partido(id): 
    resultado = db.obtener_partido(id) 

    if not resultado: 
        return jsonify({"errors": [{"code": "404", "message": f"No existe partido con ID {id}", "level": "error"}]}), 404
    
    return jsonify(resultado), 200

@app.route("/partidos/<int:id>", methods=['DELETE'])
def borrar_partido(id): 
    fila = db.borrar_partido(id) 

    if fila == 0: 
        return jsonify({"errors": [{"code": "404", "message": f"No existe partido con ID {id}", "level": "error"}]}), 404
    return '', 204

@app.route('/partidos/<int:id>/prediccion', methods=['POST'])
def agregar_prediccion(id):
    data = request.get_json()
    
    usuario_id = data.get('id_usuario')
    goles_local = data.get('local')
    goles_visitante = data.get('visitante')
    
    if usuario_id is None or goles_local is None or goles_visitante is None:
        return jsonify({'error': 'Faltan datos'}), 400
    
    result = db.agregar_prediccion(id, usuario_id, goles_local, goles_visitante)
    return jsonify(result), result.get('code', 201)

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se enviaron datos"}), 400

    nombre = datos.get("nombre")
    email  = datos.get("email")

    if not nombre or not email:
        return jsonify({"error": "Se requieren nombre y email"}), 400

    resultado = db.crear_usuario(nombre, email)

    if resultado.get("code") == 409:
        return jsonify({"error": resultado["error"]}), 409

    return jsonify({"mensaje": "Usuario creado correctamente", "id": resultado["id"]}), 201


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    limit  = request.args.get("limit",  default=10, type=int)
    offset = request.args.get("offset", default=0,  type=int)

    resultados, conteo_total = db.listar_usuarios(limit, offset)

    links = {
        "_self":  url_for("listar_usuarios", limit=limit, offset=offset,            _external=True),
        "_first": url_for("listar_usuarios", limit=limit, offset=0,                 _external=True),
    }

    if offset + limit < conteo_total:
        links["_next"] = url_for("listar_usuarios", limit=limit, offset=offset + limit, _external=True)

    if offset > 0:
        links["_prev"] = url_for("listar_usuarios", limit=limit, offset=max(0, offset - limit), _external=True)

    ultimo_offset = (conteo_total // limit) * limit
    if ultimo_offset == conteo_total and conteo_total > 0:
        ultimo_offset -= limit
    links["_last"] = url_for("listar_usuarios", limit=limit, offset=ultimo_offset, _external=True)

    return jsonify({"data": resultados, "total": conteo_total, "links": links})


@app.route("/usuarios/<int:id>", methods=["GET"])
def obtener_usuario(id):
    resultado = db.obtener_usuario(id)

    if not resultado:
        return jsonify({"errors": [{"code": "404", "message": f"No existe usuario con ID {id}", "level": "error"}]}), 404

    return jsonify(resultado), 200


@app.route("/usuarios/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    datos = request.get_json()

    if not datos:
        return jsonify({"errors": [{"code": "400", "message": "No se enviaron datos", "level": "error"}]}), 400

    nombre = datos.get("nombre")
    email  = datos.get("email")

    if not nombre or not email:
        return jsonify({"errors": [{"code": "400", "message": "Se requieren nombre y email", "level": "error"}]}), 400

    resultado = db.actualizar_usuario(id, nombre, email)

    if resultado.get("code") == 404:
        return jsonify({"errors": [{"code": "404", "message": f"No existe usuario con ID {id}", "level": "error"}]}), 404

    if resultado.get("code") == 409:
        return jsonify({"errors": [{"code": "409", "message": resultado["error"], "level": "error"}]}), 409

    return "", 204


@app.route("/usuarios/<int:id>", methods=["DELETE"])
def borrar_usuario(id):
    filas = db.borrar_usuario(id)

    if filas == 0:
        return jsonify({"errors": [{"code": "404", "message": f"No existe usuario con ID {id}", "level": "error"}]}), 404

    return "", 204