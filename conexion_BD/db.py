import pyodbc


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