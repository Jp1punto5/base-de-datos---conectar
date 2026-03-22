from flask import Flask
from flask_cors import CORS
from controlador.API_varias import varias_bp
from controlador.API_certificado import cert_bp
from controlador.API_actualizarImei import actuaImei_bp

import pyodbc

print("Drivers disponibles:", pyodbc.drivers())

app = Flask(__name__)
CORS(app)

# Registrar rutas
app.register_blueprint(varias_bp)
app.register_blueprint(cert_bp)
app.register_blueprint(actuaImei_bp)

@app.route('/')
def home():
    return "API funcionando 👌"


if __name__ == '__main__':
    print("Iniciando API...")
    app.run(debug=True, port=5000)