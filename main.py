from flask import Flask
from controllers.ranking_controller import ranking_bp
from controllers.partidos_controller import partidos_bp
from controllers.usuarios_controller import usuarios_bp

app = Flask(__name__)

app.register_blueprint(ranking_bp)
app.register_blueprint(partidos_bp)
app.register_blueprint(usuarios_bp)

@app.route('/')
def inicio():
    return "¡Hola! Este es el backend de la API del Mundial."

if __name__ == '__main__':
    app.run(debug=True)