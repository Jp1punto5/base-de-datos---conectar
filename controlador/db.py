import pyodbc

# 🔐 conexión fija (la que ya usabas)
def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=10.24.0.32;"
        "DATABASE=GPS_SALFA;"
        "UID=SaC_WisetrackCorp;"
        "PWD=A4xru7w3L4yRAwx;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)


# 🔥 conexión dinámica (la importante ahora)
def get_connection_dynamic(server, user, password, database=None):
    
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    # opcional: agregar base de datos
    if database:
        conn_str += f"DATABASE={database};"

    return pyodbc.connect(conn_str)