from flask import Blueprint, request, jsonify
from controlador.API_varias import SESIONES  # <-- reutilizamos la memoria
from conexion_BD.db import get_connection_dynamic

equip_bp = Blueprint("equipamientos", __name__)

# de aqui hacia abajo puedo crear la api

@equip_bp.route("/equipamientos", methods=["POST"])
def agregar_equipamiento():
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


                        if object_id('tempdb..#movil') is not null begin drop table #movil end 
                        if object_id('tempdb..#modelosGps') is not null begin drop table #modelosGps end
                        if object_id('tempdb..#equipamientos') is not null begin drop table #equipamientos end -- se crea como INTO dentro del proceso
                        if object_id('tempdb..#listarEqui') is not null begin drop table #listarEqui end 

                        create table #movil
                        (
                            patente varchar(20),
                            imei varchar(20)
                        )

                        create table #modelosGps 
                        (
                            imei varchar(15),
                            nombre varchar(50)
                        )

                        create table #listarEqui
                        (
                            idd int identity (1,1),
                            patente varchar(30),
                            id_equi int
                        )

                        -- vamos a insertar la patente

                        insert into #movil
                        select 
                        mov_Codigo, 
                        MOV_IDGPS 
                        from moviles 
                        where mov_Codigo = ? -- aqui va la patente
                        and MOV_IDGPS <> '9999' -- validamos que sea una unidad activa


                        -- si la unidad ya tuvo o tiene equipamientos, los eliminamos para NO entorpecer el proceso

                        delete from MOVILES_EQUIPAMIENTO where mov_Codigo in 
                        (
                                select patente from #movil
                        )
                        ----------***--------------***-----------------


                        -- insertamos los modelos de cada GPS + su identificador inicial del IMEI

                        insert into #modelosGps
                        values
                                ('20002', 'VT10'),
                                ('20212', 'VT10'),
                                ('30006', 'TRAX S10'),
                                ('30009', 'TRAX S15'),
                                ('31009', 'TRAX S15'),
                                ('30010', 'TRAX S16'),
                                ('31010', 'TRAX S16'),
                                ('30020', 'TRAX S17'),
                                ('31020', 'TRAX S17'),
                                ('30013', 'TRAX S23'),
                                ('31013', 'TRAX S23'), 
                                ('31040', 'TRAX S44'),
                                ('30040', 'TRAX S44'),
                                ('35262', 'TELTONIKA 2G FMB920/FMB910/MTB100'),
                                ('35401', 'TELTONIKA 2G FMB920/FMB910/MTB100'), 
                                ('35963', 'TELTONIKA 2G FMB920/FMB910/MTB100'), 
                                ('86014', 'TELTONIKA 3G FM3001'),
                                ('86440', 'TELTONIKA 3G FM3001'),
                                ('86706', 'TELTONIKA 3G FM3001'),
                                ('86770', 'TELTONIKA 3G FM3001'),
                                ('865413051','TELTONIKA FCMB920'),
                                ('40001', 'GV200'), 
                                ('40003', 'GMT100'), 
                                ('40004', 'GL200'), 
                                ('40008', 'GL505'), 
                                ('40009', 'GL300'),
                                ('40005', 'QUECLINK GV628'), 
                                ('40002', 'QUECLINK GV500'),
                                ('41007', 'QUECLINK GV75W'),
                                ('86480', 'QUECLINK GV75W'),
                                ('5100',  'QUECLINK GV300'),
                                ('50005', 'QUECLINK GV300'),
                                ('867035','QUECLINK GV350'),
                                ('864431','QUECLINK GV350'),
                                ('862599','QUECLINK GV350'),
                                ('860517','QUECLINK GV350'),
                                ('8646960','QUECLINK GV57'),
                                ('86508', 'QUECLINK GV50'),
                                ('45623', 'CALAMP LMU3030'), 
                                ('47643', 'CALAMP LMU2630'),  
                                ('60001', 'PORTMAN'), 	
                                ('45624','CALAMP'),		
                                ('45622','CALAMP 3030'),
                                ('76102','TABLET')
                                


                      SELECT
                        CASE 
                            WHEN MOV_FOTO LIKE '%SEÑUELO%' or MOV_FOTO LIKE '%2DO GPS SEÑUELO' THEN 41
                                END AS SENUELO,
                        CASE 
                            WHEN MOV_FOTO LIKE '%CC%' THEN 1
                                END AS CC,
                        CASE 
                            WHEN MOV_FOTO LIKE '%IBUTTON%' THEN 7
                                END AS IBUTTON,
                        CASE 
                            WHEN MOV_FOTO LIKE'%BUZZER%' OR MOV_FOTO LIKE'%+ BUZZER +%' THEN 3
                            END AS Buzzer,
                        CASE 
                            WHEN  MOV_FOTO LIKE '%+ P' or mov_foto like '% p %'  OR MOV_FOTO LIKE '%PANICO%' THEN 2
                            END AS Panico,
                        CASE 
                            WHEN  MOV_FOTO LIKE '%AIR%' THEN 9
                            END AS AIR,
                        CASE 
                            WHEN  MOV_FOTO LIKE '%FATIGA %' OR MOV_FOTO LIKE '%FATIGA%' OR MOV_FOTO LIKE '%SOMNOLENCIA%' THEN 35
                            END AS Fatiga,
                        CASE 
                                WHEN MOV_FOTO LIKE '% AIO %' OR MOV_FOTO LIKE '% AIO' THEN 62
                        END AS AIO,
                        CASE
                            WHEN MOV_FOTO LIKE '% ADAS %' OR MOV_FOTO LIKE '% ADAS' THEN 64
                        END ADAS,
                        CASE
                            WHEN MOV_FOTO LIKE '% DMS %' OR MOV_FOTO LIKE '% DMS' THEN 63
                        END DMS,
                        CASE
                            WHEN MOV_FOTO LIKE '% DRIVERZEN %' OR MOV_FOTO LIKE '% DRIVERZEN' THEN 65
                        END DRIVERZEN,
                        CASE
                            WHEN MOV_FOTO LIKE '% DRIVERZEN360 %' OR MOV_FOTO LIKE '% DRIVERZEN360' THEN 66
                        END DRIVERZEN360,
                        CASE
                            WHEN MOV_FOTO LIKE '% NESTLE %' THEN 51 -- esto es una camara de MDVR 
                        END MDVR_NESTLE,
                        case 
                                when mov_foto like '%SFRENO%' then 73
                        end SFreno,
                        CASE 
                                WHEN  MOV_FOTO LIKE '% ROADEFEND%'THEN 37
                        END AS ROADEFEND,
                        CASE 
                            WHEN MOV_FOTO LIKE '%1P%' OR MOV_FOTO LIKE '%+ 1 P%'  THEN 12
                            END AS 'PP',
                        CASE 
                            WHEN MOV_FOTO LIKE '%SKYWAVE%' OR MOV_FOTO LIKE '%ORBCOMM%' THEN 8
                            END AS 'SKYWAVE',
                        CASE 
                            WHEN MOV_FOTO LIKE '%TEMPERATURA%' OR MOV_FOTO LIKE '% T %' OR MOV_FOTO LIKE '% T' THEN 16
                            END AS 'TEMPERATURA',
                        CASE 
                            WHEN MOV_FOTO LIKE '%3ER OJO%' OR MOV_FOTO LIKE '%MDAS%' OR  MOV_FOTO LIKE '%TERCER OJO%' THEN 33
                            END AS 'OJO',
                        CASE 
                            WHEN MOV_FOTO LIKE '%MOBILEYE%' OR MOV_FOTO LIKE '% MOBILEYE %' THEN 33
                            END AS 'MOBILEYE',
                        CASE 
                            WHEN MOV_FOTO LIKE '%ACELEROMETRO%' THEN 25
                            END AS 'ACELEROMETRO',

                        CASE
                            WHEN MOV_FOTO LIKE '%2D%' THEN 32
                        END DOS_D,
                        CASE
                            WHEN MOV_FOTO LIKE '%DETEC_JAMMER%' THEN 22
                        END DETEC_JAMMER,
                        CASE
                            WHEN MOV_FOTO LIKE'%DASHCAM%' THEN 46
                        END DASHCAM,
                        CASE
                            WHEN MOV_FOTO LIKE '%Caja Negra%' OR MOV_FOTO LIKE '%caja negra%' THEN 28
                            END CN,
                        CASE
                            when m.MOV_IDGPS like '%'+gps.imei+'%' then gps.NOMBRE
                            WHEN  m.MOV_IDGPS = m.MOV_CODIGO THEN 'GPS EXTERNO'
                            ELSE GPS.NOMBRE
                        END GPS,
                        MOV_CODIGO,
                        MOV_FOTO,
                        case
                            when m.MOV_IDGPS like '%'+gps.imei+'%' then 4
                            else null
                        end  as Equipo_Gps,
                        null as 'Integracion' 
                    into #equipamientos  -- creamos tabla que contendra la información
                    FROM MOVILES M 
                    LEFT JOIN #modelosGps GPS 
                    ON MOV_IDGPS like GPS.imei+'%' 
                    WHERE MOV_IDGPS <> '9999' 
                    and m.mov_codigo in
                    (
                    select patente from #movil
                    )

                            -- validamos la existencia de la tabla de multireplicas

                            if object_id('MultiReplicas_MOVILES_TIPOINTEGRACION') is not null
                            begin
                        -- Se valida si existe alguna integración para asignar el equipamiento 68 que corresponde a este tipo de estatus

                                if exists (select top 1 * from MultiReplicas_MOVILES_TIPOINTEGRACION where ID_TipoIntegracion <> 129 and MOV_CODIGO in (select MOV_CODIGO from #movil) )
                                begin
                                    update #equipamientos
                                    set Integracion = 68 -- ID correspondiente al equipamiento "integración"
                                    where MOV_CODIGO in 
                                    (
                                    select top 1
                                        MOV_CODIGO 
                                        from MultiReplicas_MOVILES_TIPOINTEGRACION 
                                        where ID_TipoIntegracion <> 129
                                        and MOV_CODIGO in
                                        (
                                            select patente from #movil
                                        )
                                    )
                                end
                            end
                        --------------  fin del proceso ----------


                        insert into #listarEqui
                            SELECT mov_Codigo,ColumnValue
                                FROM #equipamientos
                                UNPIVOT (
                                ColumnValue FOR ColumnName IN (
                                    Equipo_Gps,
                                    CC,
                                    SENUELO,
                                    IBUTTON,
                                    Buzzer, 
                                    Panico,
                                    AIR,
                                    Fatiga,
                                    AIO,
                                    ADAS,
                                    DMS,
                                    DRIVERZEN,
                                    DRIVERZEN360,
                                    MDVR_NESTLE,
                                    sfreno,
                                    ROADEFEND,
                                    PP,
                                    SKYWAVE,
                                    TEMPERATURA,
                                    OJO,
                                    MOBILEYE,
                                    ACELEROMETRO,
                                    DOS_D,
                                    DETEC_JAMMER,
                                    DASHCAM,
                                    CN,
                                    integracion 
                                    )
                                ) AS UnpivotData


                        -- se procede a validar si existen datos para insertar --

                        if exists(select top 1 * from #listarEqui le inner join #movil m on m.patente = le.patente left join #modelosGps mg on m.imei like '%'+mg.imei+'%' LEFT JOIN [DbLink_To_fZonas].[Gps_User_Adm].[dbo].[Equipamiento] EQ on eq.id_equipamiento = le.id_equi) 
                        begin
                        ----**-----------**--------------**-------------**--------------**----------------**----------**----
                        -- se insertan los datos en la tabla moviles equipamientos
                            insert into MOVILES_EQUIPAMIENTO
                                select 
                                le.patente,
                                le.id_equi,
                                case
                                    when mg.nombre is not null and le.id_equi = 4 then mg.nombre
                                    when le.id_equi = 65 then 'DRIVERZEN'
			                        when le.id_equi = 66 then 'DRIVERZEN360'
                                    when len(eq.nombre) >50 then substring(eq.nombre,1,50) -- esto es para evitar que se caiga la inserción
                                    else eq.nombre
                                end ,
                                getdate()
                                from #listarEqui le
                                inner join #movil m
                                on m.patente = le.patente
                                left join #modelosGps mg
                                on m.imei like mg.imei+'%'
                                LEFT JOIN [DbLink_To_fZonas].[Gps_User_Adm].[dbo].[Equipamiento] EQ 
                                on eq.id_equipamiento = le.id_equi
                                
                                select 'Exito: se ingresaron los equipamientos de manera correcta' 
                        ----**-----------**--------------**-------------**--------------**----------------**----------**----
                        end
                        else
                        begin
                                select 'Error: No se puede ingresar los equipamientos'
                        end


            """

            cursor.execute(query, patente)

            while cursor.description is None:
                cursor.nextset()
                
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            resultado = []
            for row in rows:
                resultado.append(dict(zip(columns, row)))

            return jsonify({
                "columnas": columns,
                "data" : resultado
            })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
            }),500