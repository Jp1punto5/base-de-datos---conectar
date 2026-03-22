from flask import Blueprint, jsonify, request
import pyodbc
from conexion_BD.db import  get_connection_dynamic

import uuid

# 🔥 almacenamiento en memoria
SESIONES = {}

varias_bp = Blueprint('varias', __name__)


@varias_bp.route('/listar-bd', methods=['POST'])
def listar_bd():
    try:
        data = request.json
        session_id = data['session_id']

        sesion = SESIONES.get(session_id)

        if not sesion:
            return jsonify({"error": "Sesión inválida"}), 401


        with get_connection_dynamic(sesion['server'],sesion['user'],sesion['password']) as conn:

             cursor = conn.cursor()

             cursor.execute("SELECT name FROM sys.databases")
             rows = cursor.fetchall()

             databases = [row[0] for row in rows]

        return jsonify(databases)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@varias_bp.route('/estado-dispositivo', methods=['POST'])
def estado_dis():
    try:
        data = request.json
        session_id = data['session_id']

        sesion = SESIONES.get(session_id)

        if not sesion:
            return jsonify({"error":"Sesión Inválida"}) ,401

        database = data['database']
        patente  = data.get('patente','')

        with get_connection_dynamic(sesion['server'],sesion['user'],sesion['password'],database) as conn:
            cursor = conn.cursor()

            query = f"""
                select * from movil_ult_posicion where mov_Codigo = ?
            """

            cursor.execute(query,patente)
            row = cursor.fetchone()

            if not row:
                return jsonify({"reporta" : False})

            # 🔥 convertir a dict
            columns = [column[0] for column in cursor.description]
            resultado = dict(zip(columns,row))
            # 🔥 convertir datetime
            from datetime import datetime
            for key, value in resultado.items():
                if isinstance(value, datetime):
                    resultado[key] = value.strftime('%Y-%m-%d %H:%M:%S')

            return jsonify({
                    "reporta": True,
                    "data": resultado
                })
    
    except Exception as e:
        return jsonify({"error": str(e)}),500





@varias_bp.route('/tabla', methods=['POST'])
def obtener_tabla():
    try:
        data = request.json
        session_id = data['session_id']

        sesion = SESIONES.get(session_id)

        if not sesion:
            return jsonify({"error": "Sesión inválida"}), 401

        database = data['database']
        tabla = data['tabla']
        filtro1 = data.get('filtro1', '')
        filtro2 = data.get('filtropatente','')
        limite = int(data.get('limite', 10))  # 🔥 nuevo

        # ⚠️ validación básica (muy importante)
        if limite <= 0 or limite > 1000:
            limite = 10

        with get_connection_dynamic(sesion['server'],sesion['user'],sesion['password'],database) as conn:
            cursor = conn.cursor()

            # 🔥 query dinámica con límite
            query = f"SELECT TOP  {limite} * FROM {tabla}"

            if tabla == "MOVILES":
                query = f"""
                select TOP {limite}
                   *
                 from moviles
                 where mov_idgps <> '9999'"""
                if filtro1:
                    query += f" and mov_foto like '%{filtro1}%'"

                if filtro2:
                    query += f" and mov_codigo like '%{filtro2}%'"

                
            if tabla == "MOVILES_EQUIPAMIENTO":
            # ⚠️ filtro (uso controlado)
                if filtro1:
                    query += f" WHERE valor_equipamiento like '%{filtro1}%'"
                    if filtro2:
                        query += f" and mov_codigo like '%{filtro2}%'"
                
                if filtro2 and not filtro1:
                    query += f" where mov_codigo like '%{filtro2}%'"

            
            if tabla == "reportabilidad":
                query = f"""
                select 
                top {limite}

                REPLACE(M.MOV_CODIGO,'-','') as 'Movil',
                M.MOV_CODIGO AS 'Patente',
                M.MOV_IDGPS AS 'Imei o IdGPS',
                CASE 
                    WHEN UL.mopo_fechahora IS NULL THEN 'Sin información'
                    else FORMAT(UL.MOPO_FECHAHORA,'dd-MM-yyyy HH:mm:ss')
                END as 'Últ. Reporte',									
                case
                    when ul.mopo_fechahora is null then 'Sin Información'
                    else 'https://maps.google.com/maps?q='+CONVERT(VARCHAR(20),ul.MOPO_LAT)+','+CONVERT(VARCHAR(20),ul.MOPO_LON)
                end as 'Ubicación',
                case
                   WHEN MOV_SIMCARD IS NULL THEN 'Sin dato de Simcard'
                   WHEN RIGHT(MOV_SIMCARD,1) IN ('G','E','R','T','F') THEN SUBSTRING(MOV_SIMCARD,1,LEN(MOV_SIMCARD)-1)
                   ELSE MOV_SIMCARD
                end as 'Simcard',
                case
                   when MOV_FOTO like 'INS%' then FORMAT(CAST(SUBSTRING(MOV_FOTO,4,9) AS DATE),'dd-MM-yyyy')
                   when TRY_CAST(SUBSTRING(MOV_FOTO,1,10) AS date) is null then 'Revisar MOV_FOTO: ' + MOV_FOTO
                   WHEN MOV_FOTO NOT LIKE 'INS%' THEN FORMAT(CAST(SUBSTRING(MOV_FOTO,1,10) AS DATE),'dd-MM-yyyy')
                   else 'Revisar MOV_FOTO: ' + MOV_FOTO
                end as 'Fecha Instalación GPS',

                CASE 
                    WHEN M.MOV_IDGPS LIKE '86480203%' THEN 'gv75'
                    WHEN M.MOV_IDGPS LIKE '41007%' THEN 'gv75'
                    WHEN M.MOV_IDGPS LIKE '400070%' THEN 'gv75'
                    WHEN M.MOV_IDGPS LIKE '31040%' THEN 'Trax s44'
                    WHEN M.MOV_IDGPS LIKE '30040%' THEN 'Trax s44'
                    WHEN M.MOV_IDGPS LIKE '8646960%' THEN 'gv57'
                    WHEN M.MOV_IDGPS LIKE '867035%' THEN 'gv350'
                    WHEN M.MOV_IDGPS LIKE '862599%' THEN 'gv350'
                    WHEN M.MOV_IDGPS LIKE '864431%' THEN 'gv350'
                    WHEN M.MOV_IDGPS LIKE '860517%' THEN 'gv350'
                    WHEN M.MOV_IDGPS LIKE '31020%' THEN 'Trax s17'
                    WHEN M.MOV_IDGPS LIKE '31013%' THEN 'Trax s23'
                    WHEN M.MOV_IDGPS LIKE '31010%' THEN 'Trax s16'
                    WHEN M.MOV_IDGPS LIKE '5100%' THEN 'gv300'
                    WHEN M.MOV_IDGPS LIKE '865413051%' THEN 'TELTONIKA FCMB920'
                    WHEN M.MOV_IDGPS LIKE '9999' THEN 'Sin GPS'
                    ELSE 'Dispositivo no reconocido idpgs: '+ CAST(M.MOV_IDGPS as varchar)
                END +' +' +
                        case 
                                when MOV_FOTO like 'INS%'  then REPLACE(RIGHT(M.MOV_FOTO,CHARINDEX('|',REVERSE(M.MOV_FOTO))-1),'GPS +','') 
                                when TRY_CAST(SUBSTRING(MOV_FOTO,1,10) AS date) is null then  ' + No tiene soluciones'
                                when mov_foto NOT LIKE 'INS%' then  REPLACE(RIGHT(M.MOV_FOTO,CHARINDEX('|',REVERSE(M.MOV_FOTO))-1),'GPS +','') 
                                
                                else ' + No tiene soluciones'
                end  AS 'GPS + Solución',
                case
                    when ISNULL(UL.mopo_fechahora,-1) = -1 THEN 'OFFLINE - URGENTE'
                    WHEN DATEDIFF(DAY,UL.mopo_fechahora,GETDATE()) >=30 THEN 'OFFLINE'
                    else 'ONLINE'
                end as 'Estado GPS',
                case
                    when UL.mopo_fechahora IS NULL THEN 'Sin información'
                    WHEN DATEDIFF(DAY,UL.mopo_fechahora,GETDATE()) >=0 THEN CAST(DATEDIFF(DAY,UL.mopo_fechahora,GETDATE()) AS VARCHAR)
                    else null
                end as 'Días sin reportar',
                CAST(ul.mopo_vel as varchar) + ' km/hrs' as 'Velocidad',
                CASE
                    when UL.MOEV_NUMEROEVENTO = 50 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Desconexión de energía GPS / Manipulación Fisica'
                    when UL.MOEV_NUMEROEVENTO = 46 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Vehículo Apagado'
                    when UL.MOEV_NUMEROEVENTO = 28 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Apagado de Motor'
                    when UL.MOEV_NUMEROEVENTO = 29 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Encendido de Motor'
                    when UL.MOEV_NUMEROEVENTO = 45 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Vehículo Encendido'
                    when UL.MOEV_NUMEROEVENTO = 47 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Reporte sin Cobertura'
                    when UL.MOEV_NUMEROEVENTO = 90 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Movimientos con Motor Apagado'
                    when UL.MOEV_NUMEROEVENTO = 40 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Bajo Nivel de Bateria'
                    when UL.MOEV_NUMEROEVENTO = 42 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Activación Botón de Pánico'
                    WHEN UL.MOEV_NUMEROEVENTO IN (17,18) THEN CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Corte de Combustible / Habilitación de Combustible'
                    when UL.MOEV_NUMEROEVENTO IN (54, 53, 30) then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Evento Control Tag'
                    when UL.MOEV_NUMEROEVENTO = 173 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Detección de Jammer'
                    when UL.MOEV_NUMEROEVENTO = 251 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Alimentación de Energía'
                    
                    -- eventos unicos de los gv75 y gv57
                    when m.MOV_IDGPS like '86480203%' or m.MOV_IDGPS like '86469606%' then case 
                                                                                                when UL.MOEV_NUMEROEVENTO = 88 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Alerta GPS Señuelo'
                                                                                            end 
                    -- aqui entran los eventos unicos de los Trax
                    when m.MOV_IDGPS not like '86480203%' or m.MOV_IDGPS not like '86469606%' then case 
                                                                                                    when UL.MOEV_NUMEROEVENTO in (51,52,86,91,92,93,94) then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Acelerometro en 3 ejes'
                                                                                                    when UL.MOEV_NUMEROEVENTO = 31 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Identificación del Conductor - Ibutton'
                                                                                                    when UL.MOEV_NUMEROEVENTO IN (36,39) then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Cierre Sesión / off motor - Ibutton'
                                                                                                    when UL.MOEV_NUMEROEVENTO = 43 then CAST(UL.MOEV_NUMEROEVENTO as varchar)+' = Alerta - Sensor de Freno'
                                                                                            end

                    else 'Evento no identificado ' + CAST(UL.MOEV_NUMEROEVENTO as varchar)
                END AS 'N° | Evento'



                from moviles m
                left join movil_ult_posicion ul 
                on m.mov_codigo = ul.mov_Codigo
                where m.mov_idgps <> '9999'
                """

                if filtro1:
                    query += f" and m.mov_nombre like '%{filtro1}%'"
                    if filtro2:
                        query += f" and m.mov_codigo like '%{filtro2}%'"
                
                if filtro2 and not filtro1:
                    query += f" and m.mov_codigo like '%{filtro2}%'"


            cursor.execute(query)

            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            resultado = []
            for row in rows:
                resultado.append(dict(zip(columns, row)))

        return jsonify({
            "columnas" : columns,
            "data": resultado
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# EndPoint para acceder a la base de datos.

@varias_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        server = data['server']
        user = data['user']
        password = data['password']

        # probar conexión
        conn = get_connection_dynamic(server, user, password)
        conn.close()

        # generar session_id
        session_id = str(uuid.uuid4())

        # guardar sesión
        SESIONES[session_id] = {
            "server": server,
            "user": user,
            "password": password
        }

        return jsonify({"session_id": session_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500