# 🚀 Sistema Web - Gestión y Consulta de Datos

## 📌 Descripción

Este proyecto corresponde a una aplicación web completa que integra:

* 🔧 Backend desarrollado en Flask (API REST)
* 🌐 Frontend con HTML, CSS y JavaScript
* 🗄️ Conexión a base de datos SQL Server mediante `pyodbc`

El sistema permite consultar información, generar reportes (como datos de vehículos), listar bases de datos disponibles y gestionar distintos procesos mediante endpoints consumidos desde la interfaz web.

---

## 🧱 Arquitectura del sistema

El proyecto está compuesto por dos partes principales:

### 🔹 Backend (Flask API)

Encargado de:

* Exponer endpoints REST
* Procesar lógica de negocio
* Conectarse a la base de datos

### 🔹 Frontend (Vista web)

Encargado de:

* Interfaz de usuario (HTML)
* Estilos (CSS)
* Consumo de API mediante JavaScript

---

## 🛠️ Tecnologías utilizadas

### Backend:

* Python 3.x
* Flask
* Flask-CORS
* pyodbc
* SQL Server

### Frontend:

* HTML5
* CSS3
* JavaScript

---

## 📦 Requisitos previos

Antes de ejecutar el proyecto, debes tener instalado:

* Python 3.x
* pip
* (Opcional) Git

---

## ⚠️ IMPORTANTE

👉 Todos los comandos deben ejecutarse en la **carpeta raíz del proyecto**

Ejemplo correcto:

```bash
C:\Users\juan.berrios\Desktop\BASE DE DATOS - CONECTAR>
```

❌ NO ejecutar en:

* Escritorio general
* Documentos
* Carpetas internas (`/img`, `/css`, `/JS`, `/controlador`, etc.)

---

## ⚙️ Instalación paso a paso

### 1. Clonar repositorio

```bash
git clone https://github.com/Jp1punto5/base-de-datos---conectar.git
cd base-de-datos---conectar
```

---

### 2. Crear entorno virtual

```bash
python -m venv venv
```

---

### 3. Activar entorno virtual

Windows:

```bash
venv\Scripts\activate
```

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución del sistema

Desde la carpeta raíz:

```bash
python app.py
```

👉 Esto levanta el backend (API Flask)

---

## 🌐 Uso del sistema

### 🔹 Backend (API)

Endpoints disponibles (ejemplo):

* `/login`
* `/tabla`
* `/estado-dispositivo`
* `/listar-bd`
* `/certificado`
* `/equipamientos` -- En produccion

---

### 🔹 Frontend (Interfaz web)

Las vistas están en la carpeta:

```
/vista
```

Archivos principales:

* `home.html`
* `vertabla.html`

👉 Puedes:

* abrirlos directamente en el navegador
* o usarlos junto con la API en ejecución

---

## 📡 Ejemplo de consumo de API

```javascript
async function obtenerCertificado(session_id, database, "SRLL-82") {
    const res = await fetch('http://127.0.0.1:5000/certificado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id, database, "SRLL-82" }) // aqui se uso una patente, pero realmente el valor viene desde lo ingresado por usuario
    });

    const response = await res.json();

    if (!response.data || response.data.length === 0) {
        alert("No hay datos para esta patente");
        return;
    }

    console.log(response.data);
}
```

---

## 🧾 Ejemplo de respuesta

```json
{
  "data": [
    {
      "equip": "CORTE, GPS",
      "imei": "862599050059946",
      "integracion": "API - Securitas",
      "modelo": "QUECLINK GV350",
      "patente": "SRLL-82",
      "rut": "77225200-5",
      "ult_repo": "19-03-2026 21:00:45"
    }
  ]
}
```
### 📌 Campos de respuesta

- `equip`: Tipo de equipamiento instalado
- `imei`: Identificador único del dispositivo
- `integracion`: Plataformas a las cuales el vehiculo se ha integrado
- `modelo`: Modelo del dispositivo GPS
- `patente`: Patente del vehículo
- `rut`: Identificador del cliente
- `ult_repo`: Última fecha de reporte del equipo

---

## ⚙️ Configuración de base de datos

La conexión se encuentra en:

```
conexion_BD/db.py
```

Ejemplo de función de conexión dinámica:

```python
def get_connection_dynamic(server, user, password, database=None):
    
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    if database:
        conn_str += f"DATABASE={database};"

    return pyodbc.connect(conn_str)
```

---

## ⚠️ IMPORTANTE SOBRE DRIVER ODBC

Para que la conexión funcione correctamente, debes tener instalado un driver ODBC compatible con SQL Server.

### 🔍 Verificar drivers disponibles

Puedes ejecutar en Python o consola:

```python
import pyodbc
print("Drivers disponibles:", pyodbc.drivers())
```

👉 Esto mostrará los drivers instalados en tu equipo.

---

### 🧠 Ejemplo de salida

```
Drivers disponibles: ['ODBC Driver 17 for SQL Server', 'ODBC Driver 18 for SQL Server']
```

---

### ⚠️ IMPORTANTE

El nombre del driver en el código que debe coincidir EXACTAMENTE con uno de los drivers instalados.

Ejemplo:

```python
DRIVER={ODBC Driver 18 for SQL Server}
```

---

## 📁 Estructura del proyecto

```
/BASE DE DATOS - CONECTAR
│
├── app.py                        # Punto de entrada principal (Flask)
│
├── conexion_BD/
│   ├── db.py      # Conexión a base de datos
│   └── __init__.py
│
├── controlador/      # Endpoints generales (consultas/reportes)
│   ├── API_varias.py
│   ├── API_Equipamiento.py
│   ├── API_certificado.py
│   └── __init__.py
│
├── vista/       # Frontend HTML
│   ├── home.html
│   └── vertabla.html
│
├── css/    # Estilos
├── JS/     # Lógica frontend
├── img/    # Recursos visuales
│
├── requirements.txt
├── README.md
├── .gitignore
└── venv/ ❌ (NO subir)
```

---

## 📌 Notas técnicas

* Se utilizan Flask Blueprints para modularizar los endpoints
* Las consultas a base de datos se realizan mediante `pyodbc`
* El sistema está preparado para ejecutarse en entorno local

---

## 🔒 Buenas prácticas

* ❌ No subir carpeta `venv/`
* ❌ No subir credenciales sensibles
* ✅ Usar variables de entorno para configuraciones sensibles
* ✅ Ejecutar siempre con entorno virtual activo
* ✅ Mantener actualizado `requirements.txt`

---

## 🧪 Solución de problemas

### Error: ModuleNotFoundError

```bash
pip install -r requirements.txt
```

## este es solo un Tips para el futuro, con este comando puedes actualizar tu archivo requirements.txt con las nuevas importaciones
## OJO esto solo funciona teniendo activo el entorno virtual /venv/
``` bash 
pip freeze > requirements.txt 
```

---

### Error al activar entorno virtual

```bash
venv\Scripts\activate
```

---

### Problemas de conexión a base de datos

* Verificar credenciales
* Validar driver ODBC instalado
* Revisar configuración en `db.py`

---

## 👨‍💻 Autor

Juan Pablo Berrios
