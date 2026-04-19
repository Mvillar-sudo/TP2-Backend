from flask import Flask, request, jsonify
import db 

app = Flask(__name__)

@app.route("/partidos", methods=['GET'])
def obtener_partidos():
    resultados = db.obtener_partidos()
    return jsonify(resultados)



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