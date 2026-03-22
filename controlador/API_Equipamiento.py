from flask import Blueprint, request, jsonify
from usuario import SESIONES  # <-- reutilizamos la memoria
from db import get_connection_dynamic

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

                    DECLARE @TABLA_MOVILES TABLE (PATENTE VARCHAR(15))

                        INSERT INTO @TABLA_MOVILES(PATENTE)
                        SELECT MOV_CODIGO FROM MOVILES WHERE MOV_CODIGO = ?
                        AND MOV_IDGPS <> '9999'


                        DECLARE @COMPLEMENTOS VARCHAR(500),@COMPLEMENTOSRESULTADO VARCHAR(500)=''

                            IF OBJECT_ID('tempdb..#TablaComplemento') IS NOT NULL
                                BEGIN
                                    DROP TABLE #TablaComplemento
                            END

                            IF OBJECT_ID('tempdb..#TablaComplementoFin') IS NOT NULL
                                BEGIN
                                    DROP TABLE #TablaComplementoFin
                            END

                            CREATE TABLE #TablaComplementoFin
                                (
                                    Moviles VARCHAR(50),
                                    Id_Equipamiento INT,
                                    NOMBRE_GPS VARCHAR(100)

                                )

                            IF OBJECT_ID('TEMPDB..#TBL_MODELOS_GPS') IS NOT NULL
                                BEGIN
                                    DROP TABLE #TBL_MODELOS_GPS
                            END

                                CREATE TABLE #TBL_EQUIPAMIENTOS
                                (
                                    Id_Equipamiento INT,
                                    Nombre VARCHAR(50)
                                )



                                IF OBJECT_ID('TEMPDB..#TBL_EQUIPAMIENTOS') IS NOT NULL
                                BEGIN
                                    DROP TABLE #TBL_EQUIPAMIENTOS
                                END


                                CREATE TABLE #TBL_MODELOS_GPS
                                (
                                    IDIDENTITY INT IDENTITY(1,1) PRIMARY KEY,
                                    ID_GPS VARCHAR(100),
                                    NOMBRE_GPS VARCHAR(100),
                                )

                                INSERT INTO #TBL_MODELOS_GPS (ID_GPS, NOMBRE_GPS) VALUES 
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
                                ('8646960','QUECLINK GV57'),  -- nuevo módelo desde sep-2025
                                ('86508', 'QUECLINK GV50'),
                                ('45623', 'CALAMP LMU3030'), 
                                ('47643', 'CALAMP LMU2630'),  
                                ('60001', 'PORTMAN'), 	
                                ('45624','CALAMP'),		
                                ('45622','CALAMP 3030'),
                                ('76102','TABLET'),
                                ('8888','GPS EXTERNO')                                               

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
                                WHEN  MOV_FOTO LIKE '%+ P%' OR MOV_FOTO LIKE '%PANICO%' THEN 2
                                END AS Panico,
                            CASE 
                                WHEN  MOV_FOTO LIKE '%AIR%' THEN 9
                                END AS AIR,
                            CASE 
                                WHEN  MOV_FOTO LIKE '%FATIGA %' OR MOV_FOTO LIKE '%FATIGA%' OR MOV_FOTO LIKE '%SOMNOLENCIA%' THEN 35
                                END AS Fatiga,
                        --------------------------------------
                        ---- NUEVOS EQUIPAMIENTOS
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

                        ---------------------------------------

                        -- Nuevo equipamiento desde el 18 de dic 2025

                        case 
                                when mov_foto like '%SFRENO%' then 73
                        end SFreno,

                        --------------------------------


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
                                WHEN GPS.NOMBRE_GPS IS NULL THEN 'MODELO NO ENCONTRADO'
                                WHEN M.MOV_IDGPS = '8888' THEN 'GPS DE OTRO PROV.'
                            ELSE GPS.NOMBRE_GPS
                            END GPS,
                            CASE
                                WHEN SUBSTRING(MOV_FOTO,1, CHARINDEX(' ', MOV_FOTO + '  ') - 1) = 'INS' THEN SUBSTRING(MOV_FOTO,1,13)
                                WHEN SUBSTRING(MOV_FOTO,1, CHARINDEX(' ', MOV_FOTO + '  ') - 1) = 'DESINST' THEN  SUBSTRING(MOV_FOTO,1,CASE 
                                                                                                                                            WHEN RIGHT(LEFT(MOV_FOTO, 18), 1) = '|' THEN CHARINDEX('|', MOV_FOTO) -1
                                                                                                                                            WHEN ISNUMERIC( RIGHT(LEFT(MOV_FOTO, 18), 1)) =1 THEN 18
                                                                                                                                            WHEN ISNUMERIC( RIGHT(LEFT(MOV_FOTO, 18), 1)) =0 THEN 17
                                                                                                                                        END  )
                            END AS DATOS,
                                MOV_CODIGO,
                                MOV_FOTO,
                                4 as Equipo_Gps,
                                null as 'Integracion' -- nueva columna para agregar equipamiento integración | 09 sep 25
                            INTO #TablaComplemento
                            FROM MOVILES M 
                                LEFT JOIN #TBL_MODELOS_GPS GPS 
                                ON MOV_IDGPS like GPS.ID_GPS+'%' -- nueva modificación para que la busqueda sea mejor | 18 jun 25
                                WHERE MOV_IDGPS <> '9999' 
                                and  MOV_CODIGO in 
                            (
                                SELECT PATENTE FROM @TABLA_MOVILES
                            )
                                GROUP BY MOV_FOTO,MOV_CODIGO,MOV_IDGPS,NOMBRE_GPS

                        -- nuevo bloque que valida la existencia de una integración, con la finalidad de asignar el valor del equipamiento 
                                if exists (select top 1 * from MultiReplicas_MOVILES_TIPOINTEGRACION where ID_TipoIntegracion <> 129 and MOV_CODIGO in (select MOV_CODIGO from #TablaComplemento) )
                                begin
                                    update #TablaComplemento
                                    set Integracion = 68 -- ID correspondiente al equipamiento "integración"
                                    where MOV_CODIGO in 
                                    (
                                    select 
                                        MOV_CODIGO 
                                        from MultiReplicas_MOVILES_TIPOINTEGRACION 
                                        where ID_TipoIntegracion <> 129
                                        and MOV_CODIGO in
                                        (
                                            select MOV_CODIGO from #TablaComplemento
                                        )
                                    )
                                end
                        --------------  fin del proceso ----------


                            ----SEPARAMOS LOS DATOS EN FILAS DISTINTAS RESPETANDO EL MOVIL
                            INSERT INTO #TablaComplementoFin
                                SELECT MOV_CODIGO,ColumnValue,GPS
                                FROM #TablaComplemento
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
                                    -- nuevos --
                                    AIO,
                                    ADAS,
                                    DMS,
                                    DRIVERZEN,
                                    DRIVERZEN360,
                                    MDVR_NESTLE,
                                    -- fin nuevos --

                                    -- nuevo 18dic25 --
                                    sfreno,
                                    -- fin nuevo 18dic25 --
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
                                    integracion -- nuevo equipamiento 09 sep 25
                                    )
                                ) AS UnpivotData


                            DECLARE @Counter INT , @counttabla int 

                            IF OBJECT_ID('tempdb..#TablaIndividual') IS NOT NULL
                                BEGIN
                                    DROP TABLE #TablaIndividual
                            END

                            SELECT
                                ROW_NUMBER() OVER(ORDER BY Moviles) AS fila,
                                --ROW_NUMBER() OVER(PARTITION BY Moviles ORDER BY Moviles) AS fila,
                                Moviles,
                                Id_Equipamiento
                            INTO #TablaIndividual
                            FROM #TablaComplementoFin


                            select @counttabla = @@ROWCOUNT

                                SET @Counter=1

                            WHILE ( @Counter <= @counttabla)
                            BEGIN
                                declare   @MOV_cod varchar (10), -- si el largo del mov_codigo es superior a 10, no se insertara nada
                                        @id_equipa int,
                                        @busqueda int,
                                        @Counter2 INT = 1,
                                        @fila int
                                
                                SELECT @MOV_cod =Moviles,@id_equipa=Id_Equipamiento from #TablaIndividual where fila=@Counter 

                                --SELECT * FROM #TablaIndividual where fila=@Counter 

                                        IF EXISTS (select top 1 1 from MOVILES_EQUIPAMIENTO WITH(NOLOCK) where  Mov_Codigo = @MOV_cod AND Id_Equipamiento =@id_equipa )
                                            BEGIN 

                                            DECLARE @MOV_cod2 varchar (10), -- si el largo del mov_codigo es superior a 10, no se insertara nada
                                                    @id_equipa2 int,
                                                    @Valor_Equipamiento varchar(MAX),
                                                    @Fecha_Insertado DATETIME

                                            SELECT
                                            @MOV_cod2=  TC.Moviles
                                                ,@id_equipa2=EQ.Id_Equipamiento
                                                ,@Valor_Equipamiento =
                                                
                                                                                    CASE 
                                                                                            
                                                                                            when EQ.Id_Equipamiento = 1	 then 'Corte Combustible'
                                                                                            when EQ.Id_Equipamiento = 2	 then 'Boton de Panico'
                                                                                            when EQ.Id_Equipamiento = 3	 then 'Buzzer'
                                                                                            when EQ.Id_Equipamiento = 4	 then TC.NOMBRE_GPS
                                                                                            when EQ.Id_Equipamiento = 7	 then 'Identificador Conductor_Kit Ibutton'
                                                                                            when EQ.Id_Equipamiento = 8	 then 'Equipo Satelital'
                                                                                            when EQ.Id_Equipamiento = 9	 then 'Alert In Route'
                                                                                            when EQ.Id_Equipamiento = 10 then 'Teclado'
                                                                                            when EQ.Id_Equipamiento = 11 then 'MDVR_Monitor'
                                                                                            when EQ.Id_Equipamiento = 12 then 'MDVR_UPS'
                                                                                            when EQ.Id_Equipamiento = 13 then 'Sensor Magnetico (Puerta) 1'
                                                                                            when EQ.Id_Equipamiento = 14 then 'Sensor Magnetico (Puerta) 2'
                                                                                            when EQ.Id_Equipamiento = 15 then 'Sensor Magnetico (Puerta) 3'
                                                                                            when EQ.Id_Equipamiento = 16 then 'Sensor Temperatura 1'
                                                                                            when EQ.Id_Equipamiento = 17 then 'Sensor Temperatura 2'
                                                                                            when EQ.Id_Equipamiento = 18 then 'Sensor Temperatura 3'
                                                                                            when EQ.Id_Equipamiento = 19 then 'Bloqueo Quinta Rueda'
                                                                                            when EQ.Id_Equipamiento = 20 then 'Cerradura Randomica'
                                                                                            when EQ.Id_Equipamiento = 21 then 'Panel Solar'
                                                                                            when EQ.Id_Equipamiento = 22 then 'Deteccion de Jammer'
                                                                                            when EQ.Id_Equipamiento = 23 then 'Cinturon de Seguridad'
                                                                                            when EQ.Id_Equipamiento = 24 then 'MiGPS Connect'
                                                                                            when EQ.Id_Equipamiento = 25 then 'Acelerometro'
                                                                                            when EQ.Id_Equipamiento = 27 then 'Bloqueo Pasajeros'
                                                                                            when EQ.Id_Equipamiento = 28 then 'Caja Negra'
                                                                                            when EQ.Id_Equipamiento = 29 then 'Can'
                                                                                            when EQ.Id_Equipamiento = 30 then 'Contador de Pasajeros'
                                                                                            when EQ.Id_Equipamiento = 31 then 'Horometro'
                                                                                            when EQ.Id_Equipamiento = 32 then 'Identificador Conductor_Lector 2D'
                                                                                            when EQ.Id_Equipamiento = 33 then 'Tercer Ojo (Mobileye)'
                                                                                            when EQ.Id_Equipamiento = 34 then 'Motor Vibrador'
                                                                                            when EQ.Id_Equipamiento = 35 then 'Sensor de Fatiga_MR688'
                                                                                            when EQ.Id_Equipamiento = 36 then 'Replica'
                                                                                            when EQ.Id_Equipamiento = 37 then 'Sensor de Fatiga_Roadefend'
                                                                                            when EQ.Id_Equipamiento = 38 then 'Sensor de Humedad'
                                                                                            when EQ.Id_Equipamiento = 40 then 'GPS Seguridad'
                                                                                            when EQ.Id_Equipamiento = 41 then 'GPS Señuelo'
                                                                                            when EQ.Id_Equipamiento = 42 then 'Tamper'
                                                                                            when EQ.Id_Equipamiento = 43 then 'Sensor Tolva'
                                                                                            when EQ.Id_Equipamiento = 46 then 'Dashcam'
                                                                                            when EQ.Id_Equipamiento = 50 then 'MDVR_Camara Interior'
                                                                                            when EQ.Id_Equipamiento = 51 then 'MDVR'
                                                                                            when EQ.Id_Equipamiento = 52 then 'MDVR_Camara Exterior'
                                                                                            when EQ.Id_Equipamiento = 56 then 'Kit Seguridad'
                                                                                            when EQ.Id_Equipamiento = 57 then 'Bateria Móvil'
                                                                                            when EQ.Id_Equipamiento = 58 then 'Bateria Equipo'
                                                                                            when EQ.Id_Equipamiento = 59 then 'Sensor Magnetico (Puerta carga lateral) 4'
                                                                                            when EQ.Id_Equipamiento = 60 then 'Sensor Magnetico (Puerta carga lateral) 5'
                                                                                            when EQ.Id_Equipamiento = 61 then 'Sensor Magnetico (Puerta carga lateral) 6'
                                                                                            when EQ.Id_Equipamiento = 62 then 'MOBICUA_All in one'
                                                                                            when EQ.Id_Equipamiento = 63 then 'Sensor Fatiga_Mobicua DMS'
                                                                                            when EQ.Id_Equipamiento = 64 then 'Tercer Ojo (Mobicua ADAS)'
                                                                                            when EQ.Id_Equipamiento = 65 then 'Driver Zen'
                                                                                            when EQ.Id_Equipamiento = 66 then 'Driver Zen 360'
                                                                                            when EQ.Id_Equipamiento = 67 then 'Tercer Ojo (MDAS 9)'
                                                                                            when EQ.Id_Equipamiento = 68 then 'Integración'   
                                                                                            when EQ.id_equipamiento = 73 then 'Sensor de Freno'
                                                                                        
                                                            
                                                                                    ELSE 'Revisar Equip.'
                                                                                    END ,
                                                @Fecha_Insertado =GETDATE()
                                            FROM  #TablaIndividual TI
                                            JOIN #TablaComplementoFin TC ON TC.Moviles = TI.Moviles AND TC.Id_Equipamiento = TI.Id_Equipamiento
                                            --LEFT JOIN [Gps_User_Adm_TT].[dbo].[Equipamiento] EQ ON  EQ.Id_Equipamiento = TC.Id_Equipamiento
                                            LEFT JOIN [DbLink_To_fZonas].[Gps_User_Adm].[dbo].[Equipamiento] EQ ON  EQ.Id_Equipamiento = TC.Id_Equipamiento
                                                WHERE TI.Moviles=@MOV_cod 
                                                AND TI.Id_Equipamiento=@id_equipa

                                                GROUP BY TC.Moviles ,TC.Id_Equipamiento,EQ.Id_Equipamiento,EQ.Nombre,TC.NOMBRE_GPS,TI.Id_Equipamiento
                                                ORDER BY TC.Moviles DESC
                                            
                                            UPDATE MOVILES_EQUIPAMIENTO
                                                SET Valor_Equipamiento =@Valor_Equipamiento
                                                ,Fecha_Insertado =@Fecha_Insertado
                                            WHERE Mov_Codigo=@MOV_cod2 AND Id_Equipamiento =@id_equipa2
                                            
                                            END
                                        ELSE
                                            BEGIN
                                            INSERT INTO  MOVILES_EQUIPAMIENTO (Mov_Codigo, Id_Equipamiento, Valor_Equipamiento, Fecha_Insertado)
                                            SELECT
                                                TC.Moviles
                                                ,EQ.Id_Equipamiento
                                                ,CASE 
                                                                                            
                                                                    when EQ.Id_Equipamiento = 1	 then 'Corte Combustible'
                                                                    when EQ.Id_Equipamiento = 2	 then 'Boton de Panico'
                                                                    when EQ.Id_Equipamiento = 3	 then 'Buzzer'
                                                                    when EQ.Id_Equipamiento = 4	 then TC.NOMBRE_GPS
                                                                    when EQ.Id_Equipamiento = 7	 then 'Identificador Conductor_Kit Ibutton'
                                                                    when EQ.Id_Equipamiento = 8	 then 'Equipo Satelital'
                                                                    when EQ.Id_Equipamiento = 9	 then 'Alert In Route'
                                                                    when EQ.Id_Equipamiento = 10 then 'Teclado'
                                                                    when EQ.Id_Equipamiento = 11 then 'MDVR_Monitor'
                                                                    when EQ.Id_Equipamiento = 12 then 'MDVR_UPS'
                                                                    when EQ.Id_Equipamiento = 13 then 'Sensor Magnetico (Puerta) 1'
                                                                    when EQ.Id_Equipamiento = 14 then 'Sensor Magnetico (Puerta) 2'
                                                                    when EQ.Id_Equipamiento = 15 then 'Sensor Magnetico (Puerta) 3'
                                                                    when EQ.Id_Equipamiento = 16 then 'Sensor Temperatura 1'
                                                                    when EQ.Id_Equipamiento = 17 then 'Sensor Temperatura 2'
                                                                    when EQ.Id_Equipamiento = 18 then 'Sensor Temperatura 3'
                                                                    when EQ.Id_Equipamiento = 19 then 'Bloqueo Quinta Rueda'
                                                                    when EQ.Id_Equipamiento = 20 then 'Cerradura Randomica'
                                                                    when EQ.Id_Equipamiento = 21 then 'Panel Solar'
                                                                    when EQ.Id_Equipamiento = 22 then 'Deteccion de Jammer'
                                                                    when EQ.Id_Equipamiento = 23 then 'Cinturon de Seguridad'
                                                                    when EQ.Id_Equipamiento = 24 then 'MiGPS Connect'
                                                                    when EQ.Id_Equipamiento = 25 then 'Acelerometro'
                                                                    when EQ.Id_Equipamiento = 27 then 'Bloqueo Pasajeros'
                                                                    when EQ.Id_Equipamiento = 28 then 'Caja Negra'
                                                                    when EQ.Id_Equipamiento = 29 then 'Can'
                                                                    when EQ.Id_Equipamiento = 30 then 'Contador de Pasajeros'
                                                                    when EQ.Id_Equipamiento = 31 then 'Horometro'
                                                                    when EQ.Id_Equipamiento = 32 then 'Identificador Conductor_Lector 2D'
                                                                    when EQ.Id_Equipamiento = 33 then 'Tercer Ojo (Mobileye)'
                                                                    when EQ.Id_Equipamiento = 34 then 'Motor Vibrador'
                                                                    when EQ.Id_Equipamiento = 35 then 'Sensor de Fatiga_MR688'
                                                                    when EQ.Id_Equipamiento = 36 then 'Replica'
                                                                    when EQ.Id_Equipamiento = 37 then 'Sensor de Fatiga_Roadefend'
                                                                    when EQ.Id_Equipamiento = 38 then 'Sensor de Humedad'
                                                                    when EQ.Id_Equipamiento = 40 then 'GPS Seguridad'
                                                                    when EQ.Id_Equipamiento = 41 then 'GPS Señuelo'
                                                                    when EQ.Id_Equipamiento = 42 then 'Tamper'
                                                                    when EQ.Id_Equipamiento = 43 then 'Sensor Tolva'
                                                                    when EQ.Id_Equipamiento = 46 then 'Dashcam'
                                                                    when EQ.Id_Equipamiento = 50 then 'MDVR_Camara Interior'
                                                                    when EQ.Id_Equipamiento = 51 then 'MDVR'
                                                                    when EQ.Id_Equipamiento = 52 then 'MDVR_Camara Exterior'
                                                                    when EQ.Id_Equipamiento = 56 then 'Kit Seguridad'
                                                                    when EQ.Id_Equipamiento = 57 then 'Bateria Móvil'
                                                                    when EQ.Id_Equipamiento = 58 then 'Bateria Equipo'
                                                                    when EQ.Id_Equipamiento = 59 then 'Sensor Magnetico (Puerta carga lateral) 4'
                                                                    when EQ.Id_Equipamiento = 60 then 'Sensor Magnetico (Puerta carga lateral) 5'
                                                                    when EQ.Id_Equipamiento = 61 then 'Sensor Magnetico (Puerta carga lateral) 6'
                                                                    when EQ.Id_Equipamiento = 62 then 'MOBICUA_All in one'
                                                                    when EQ.Id_Equipamiento = 63 then 'Sensor Fatiga_Mobicua DMS'
                                                                    when EQ.Id_Equipamiento = 64 then 'Tercer Ojo (Mobicua ADAS)'
                                                                    when EQ.Id_Equipamiento = 65 then 'Driver Zen'
                                                                    when EQ.Id_Equipamiento = 66 then 'Driver Zen 360'
                                                                    when EQ.Id_Equipamiento = 67 then 'Tercer Ojo (MDAS 9)'
                                                                    when EQ.Id_Equipamiento = 68 then 'Integración'        
                                                                    when EQ.id_equipamiento = 73 then 'Sensor de Freno'
                                                                                        
                                                            
                                                            ELSE 'Revisar Equip.'
                                                        END Valor_Equipamiento,
                                                GETDATE() Fecha_Insertado
                                            FROM  #TablaIndividual TI
                                            JOIN #TablaComplementoFin TC ON TC.Moviles = TI.Moviles AND TC.Id_Equipamiento = TI.Id_Equipamiento
                                            LEFT JOIN [DbLink_To_fZonas].[Gps_User_Adm].[dbo].[Equipamiento] EQ ON  EQ.Id_Equipamiento = TC.Id_Equipamiento
                                            WHERE TI.Moviles=@MOV_cod AND TI.Id_Equipamiento=@id_equipa
                                            GROUP BY TC.Moviles ,TC.Id_Equipamiento,EQ.Id_Equipamiento,EQ.Nombre,TC.NOMBRE_GPS,TI.Id_Equipamiento
                                            ORDER BY TC.Moviles DESC

                                    END
                                    
                                    SET @Counter =@Counter +1 

                            END




            """

            cursor.execute(query, patente)

            conn.commit()  # 🔥 IMPORTANTE

            return jsonify({
                "ok": True,
                "mensaje": "Equipamiento procesado correctamente"
            })
    
    except Exception as e:
        return jsonify({"error": str(e)}),500