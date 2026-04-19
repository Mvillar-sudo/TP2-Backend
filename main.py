from flask import Flask
from controllers.ranking_controller import ranking_bp

app = Flask(__name__)

app.register_blueprint(ranking_bp)

@app.route('/')
def inicio():
    return "¡Hola! Este es el backend de la API del Mundial."

if __name__ == '__main__':
    app.run(debug=True)