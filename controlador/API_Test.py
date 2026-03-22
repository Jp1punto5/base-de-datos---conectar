from flask import Flask
from flask_cors import CORS
from usuario import usuarios_bp
from API_certificado import cert_bp

import pyodbc

print("Drivers disponibles:", pyodbc.drivers())

app = Flask(__name__)
CORS(app)

# Registrar rutas
app.register_blueprint(usuarios_bp)
app.register_blueprint(cert_bp)

@app.route('/')
def home():
    return "API funcionando 👌"


if __name__ == '__main__':
    print("Iniciando API...")
    app.run(debug=True, port=5000)