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
git clone https://github.com/TU-USUARIO/TU-REPO.git
cd TU-REPO
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

Se accede mediante endpoints REST, por ejemplo:

* `/equipamientos`
* `/certificado`
* `/bases-datos`
* `/vehiculos`

---

### 🔹 Frontend (Interfaz web)

Las vistas están en la carpeta:

```bash 
/vista
```

Archivos principales:

* `home.html`
* `vertabla.html`

👉 Para usarlas:

* abrir directamente en navegador
* o integrarlas con el backend en ejecución

---

## 📁 Estructura del proyecto

```bash 
/BASE DE DATOS - CONECTAR
│
├── app.py                        # Punto de entrada principal (Flask)
│
├── conexion_BD/
│   └── db.py                     # Conexión a base de datos
│
├── controlador/
│   ├── API_varias.py             # Endpoints generales (consultas/reportes)
│   ├── API_Equipamiento.py
│   ├── API_certificado.py
│
├── vista/                        # Frontend HTML
│   ├── home.html
│   └── vertabla.html
│
├── css/                          # Estilos
├── JS/                           # Lógica frontend
├── img/                          # Recursos visuales
│
├── requirements.txt
├── README.md
├── .gitignore
└── venv/ ❌ (NO subir)
```

---

## ⚙️ Configuración

* Configurar conexión a base de datos en:

  * `conexion_BD/db.py`
* Verificar credenciales y acceso a SQL Server

---

## 🔒 Buenas prácticas

* ❌ No subir carpeta `venv/`
* ❌ No subir credenciales
* ✅ Ejecutar siempre con entorno virtual activo
* ✅ Mantener actualizado `requirements.txt`

---

## 🧪 Solución de problemas

### Error: ModuleNotFoundError

```bash 
pip install -r requirements.txt
```

---

### Error al activar entorno virtual

```bash 
venv\Scripts\activate
```

---

### Problemas de conexión a base de datos

* Verificar credenciales
* Revisar servidor SQL
* Validar configuración en `db.py`

---

## 👨‍💻 Autor

Juan Pablo Berrios
