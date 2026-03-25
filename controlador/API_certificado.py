from flask import Blueprint, request, jsonify
from controlador.API_varias import SESIONES  # <-- reutilizamos la memoria
from conexion_BD.db import get_connection_dynamic

cert_bp = Blueprint("certificados", __name__)

# de aqui hacia abajo puedo crear la api

@cert_bp.route("/certificado", methods=["POST"])
def crear_certificado():
    try:
        data = request.json
        session_id = data['session_id']

        sesion = SESIONES.get(session_id)

        if not sesion:
            return jsonify({"error":"Sesión Inválida"}) ,401

        database = data['database']
        patente  = data.get('patenteFinal','')

        with get_connection_dynamic(sesion['server'],sesion['user'],sesion['password'],database) as conn:
            cursor = conn.cursor()

            query = """
            if object_id('tempdb..#certificado') is not null begin drop table #certificado end
            if object_id('tempdb..#equipamiento') is not null begin drop table #equipamiento end
            if object_id('tempdb..#integracion') is not null begin drop table #integracion end


            create table #certificado
            (
                patente varchar(30),
                imei varchar(30),
                modelo varchar(60),
                ult_repo varchar(50),
                equip varchar(max),
                integracion varchar(max),
                rut varchar(30)
            )

            create table #equipamiento
            (
            idd int identity(1,1),
            patente varchar(30),
            equip varchar(max)
            )

            create table #integracion
            (
            idd int identity(1,1),
            patente varchar(30),
            intregra varchar(max)
            )


            -- variables ciclo while

            declare @numin int, @numfin int,
                
                @patente varchar (30) = ?  -- aqui va la patente

            -- insertamos patente, IDGPS y Rut
            insert into #certificado (patente,imei,rut)
            select
            mov_codigo,
            MOV_IDGPS,
            mov_rut
            from moviles where mov_Codigo = @patente

            -- insertamos modelo del GPS
            update ce 
            set ce.modelo = me.Valor_Equipamiento
            from #certificado ce
            inner join MOVILES_EQUIPAMIENTO me 
            on me.Mov_Codigo = ce.patente
            where mov_Codigo = @patente
            and Id_Equipamiento = 4


            -- insertamos ultima posición
            update ce  
                set ce.ult_repo =
                                    case
                                        when ul.mopo_fechahora is null then 'Sin Información'
                                        else format(ul.mopo_fechahora,'dd-MM-yyyy HH:mm:ss')
                                    end 
                from #certificado ce
                left join MOVIL_ULT_POSICION ul
                on ce.patente = ul.mov_codigo
                where ce.patente = @patente

                -- insertamos todos los equipamientos para procesarlos

                insert into #equipamiento(patente,equip)
                select 
                mov_codigo,
                case 
                    when Id_Equipamiento = 1 then 'CORTE'
                    when Id_Equipamiento = 4 then 'GPS'
                    when Id_Equipamiento = 62 then 'MOBICUA AIO (SOMNOLENCIA + TERCER OJO)'
                    when Id_Equipamiento = 63 then 'MOBICUA DMS (SOMNOLENCIA)'
                    when Id_Equipamiento = 64 then 'MOBICUA ADAS (TERCER OJO)'
                    when Id_Equipamiento = 65 then 'DRIVERZEN (SOMNOLENCIA + TERCER OJO + CÁMARA FRONTAL)'
                    when Id_Equipamiento = 66 then 'DRIVENZEN 360 (SOMNOLENCIA + TERCER OJO + CÁMARA FRONTAL + CÁMARA EN CABINA)'
                    when id_equipamiento = 51 then 'CÁMARA MDVR'
                    when id_equipamiento = 25 then 'ACELERÓMETRO 3 EJES'
                    else Valor_Equipamiento

                end as 'Equipamiento'
                from MOVILES_EQUIPAMIENTO
                where mov_Codigo = @patente
                and Id_Equipamiento <> 68

                -- comenzamos 1er ciclo while

                select @numin = min(idd), @numfin = max(idd) from #equipamiento

                while @numin <= @numfin
                begin
                    
                    if (select equip from #certificado where patente = @patente) is null
                    begin
                        update ce 
                        set ce.equip = eq.equip
                        from #certificado ce
                        inner join #equipamiento eq
                        on ce.patente = eq.patente
                        where eq.idd = @numin
                    end
                    else
                    begin
                        update ce 
                        set ce.equip = ce.equip + ', '+ eq.equip
                        from #certificado ce
                        inner join #equipamiento eq
                        on ce.patente = eq.patente
                        where eq.idd = @numin

                    end

                    set @numin = @numin + 1
                end



                -- vamos a insertar todas las integraciones para procesarlas

                insert into #integracion (patente,intregra)
                select
                    mu.MOV_CODIGO,
                    case 
                            WHEN ID_TipoIntegracion = 4 THEN 'Bechtel QB'
                            WHEN ID_TipoIntegracion = 5 THEN 'Redd'
                            WHEN ID_TipoIntegracion = 13 THEN 'Waypoint'
                            WHEN ID_TipoIntegracion = 20 THEN 'Ctac Informática TMS - Collahuasi' 
                            WHEN ID_TipoIntegracion IN (25,74) THEN 'AVL Control'
                            WHEN ID_TipoIntegracion = 29 THEN 'Centinela' -- dada de baja
                            WHEN ID_TipoIntegracion = 37 THEN 'Gauss Control' -- Esta esta dada de baja
                            WHEN ID_TipoIntegracion = 45 THEN 'Qanalityc'
                            WHEN ID_TipoIntegracion = 47 THEN 'GPSChile - (GPS)'
                            WHEN ID_TipoIntegracion IN (53,54,97) THEN 'BHP'
                            WHEN ID_TipoIntegracion = 50 THEN 'AVL'
                            WHEN ID_TipoIntegracion = 62 THEN 'FCAB'
                            WHEN ID_TipoIntegracion = 64 THEN 'Drive.in'
                            WHEN ID_TipoIntegracion = 70 THEN 'GeoConexion'
                            WHEN ID_TipoIntegracion = 72 THEN 'Ausenco' -- esta dada de baja
                            WHEN ID_TipoIntegracion = 80 THEN 'Codelco'
                            WHEN ID_TipoIntegracion = 86 THEN 'Antucoya' -- dada de baja
                            WHEN ID_TipoIntegracion = 89 THEN 'Salvador'
                            WHEN ID_TipoIntegracion = 91 THEN 'Bechtel Collahuasi'
                            WHEN ID_TipoIntegracion = 94 THEN 'TrackTec'
                            WHEN ID_TipoIntegracion = 95 THEN 'Skynav-Centinela'
                            WHEN ID_TipoIntegracion = 98 THEN 'Lomas Bayas'
                            WHEN ID_TipoIntegracion = 107 THEN 'OWL CASERONES'
                            WHEN ID_TipoIntegracion = 41 THEN 'Samtech (Codelco) - ' + 
                                                                                        case
                                                                                            when mu.MVTI_OPCIONAL_1 = 'codelcodch' then 'Faena (DCH)'
                                                                                            when mu.MVTI_OPCIONAL_1 = 'codelcodgm' then 'Faena (DGM)'
                                                                                            when mu.MVTI_OPCIONAL_1 = 'codelcodn' then 'Faena (DMH)'
                                                                                            when mu.MVTI_OPCIONAL_1 = 'cimcmz' then 'Faena (CIMZ Zaldivar)'
                                                                                        end 
                                            
                            WHEN ID_TipoIntegracion = 87 THEN 'API Waypoint GO - Chilexpress'
                            WHEN ID_TipoIntegracion = 83 THEN 'API - TECNOGPS'
                            WHEN ID_TipoIntegracion = 110 THEN 'API - TRACKTEC MEL BHP'
                            WHEN ID_TipoIntegracion = 111 THEN 'API - OWL CODELCO (El Teniente)'
                            WHEN ID_TipoIntegracion = 113 THEN 'API - SKYNAV ANTUCOYA'
                            WHEN ID_TipoIntegracion = 115 THEN 'API - SKYNAV GUINEZ'
                            WHEN ID_TipoIntegracion = 130 THEN 'API - SKYNAV PELAMBRES'
                    end as 'integracion'
                    from MultiReplicas_MOVILES_TIPOINTEGRACION mu
                    inner join MultiReplicas_MOVILES m
                    on m.MOV_CODIGO = mu.MOV_CODIGO
                    where m.MOV_CODIGO = @patente
                    and m.ESTADO = 1
                    and mu.ID_TipoIntegracion not in (84,103,129)


                    -- identificamos si existe la integracion de gausscontrol o GPSChile Mobicua

                    if object_id('gausscontrol_moviles') is not null
                    begin
                    -- gausscontrol
                        insert into #integracion (patente,intregra)
                         select 
                            m.mov_codigo,
                            'API - GaussControl - MOBICUA' as 'Api GaussControl Mobicua'
                            from MOVILES m
                            inner join GaussControl_MOVILES gm 
                            on m.MOV_CODIGO = gm.MOV_CODIGO
                            where m.MOV_codigo = @patente
                            and gm.ESTADO =  1
                    end

                    if object_id('WinS_GpsChileFatiga_Moviles') is not null
                    begin
                        -- GPSChile Mobicua
                         insert into #integracion (patente,intregra)
                          select 
                            m.MOV_CODIGO as 'Patente',
                            'API - GPSChile - MOBICUA (FATIGA)' as 'Nombre API'  -- Tecnasic / Fatiga (videos y fotos)
                            from WinS_GpsChileFatiga_Moviles ft
                            inner join MOVILES m
                            on ft.Mov_Codigo = m.MOV_CODIGO
                            where m.MOV_CODIGO = @patente
                    end

                                ------------------------------------------


                    --- insertamos la API de Securitas si aplica con la patente
                    insert into #integracion (patente,intregra)
                    select	
                        fm.cod_interno ,
                        'API - Securitas' as 'Nombre API'-- Securitas
                        from MOVILES m
                        inner join FLEET_MOV_ASIGNADOS fm 
                        on m.MOV_CODIGO = fm.Cod_interno
                        inner join FLEET_USUARIOS fu 
                        on fu.USU_ID = fm.USU_ID
                        where fu.USU_USER = 'SECU_CHI' -- nombre usuario API 
                        and m.MOV_CODIGO = @patente

                    ---------------------------------------


                    --- insertamos la integracion de Kaufmann si es que aplica con la patente

                    insert into #integracion (patente,intregra)
                    select
                    mov_codigo,
                    'API - KAUFMANN' as 'Nombre API'
                    from moviles 
                    where mov_idgps <> '9999'
                    and mov_foto like '%kaufmann%'
                    and MOV_CODIGO = @patente

                    --------------------------------------


                    -- insertamos la API de MaqSur si aplica con la patente
                    insert into #integracion (patente,intregra)
                    select	
                        fm.cod_interno ,
                        'API - MaqSur' as 'Nombre API'-- MaqSur
                        from MOVILES m
                        inner join FLEET_MOV_ASIGNADOS fm 
                        on m.MOV_CODIGO = fm.Cod_interno
                        inner join FLEET_USUARIOS fu 
                        on fu.USU_ID = fm.USU_ID
                        where fu.USU_USER = 'api_maqsur' -- nombre usuario API 
                        and m.MOV_CODIGO = @patente


                -----------------------------------



                -- asignamos numero inicial y final para el ciclo while
                select @numin = min(idd), @numfin = max(idd) from #integracion
                -- comenzamos ciclo while
                while @numin <= @numfin
                begin
                    
                    if (select integracion from #certificado where patente = @patente) is null
                    begin
                        update ce 
                        set ce.integracion = it.intregra
                        from #certificado ce
                        inner join #integracion it
                        on ce.patente = it.patente
                        where it.idd = @numin
                    end
                    else
                    begin
                        update ce 
                        set ce.integracion = ce.integracion + ', '+ it.intregra
                        from #certificado ce
                        inner join #integracion it
                        on ce.patente = it.patente
                        where it.idd = @numin

                    end

                    set @numin = @numin + 1
                end


                -- retornamos los datos para el certificado
                select * from #certificado
            
            """

            cursor.execute(query,patente)
            # 🔥 IMPORTANTE
            while cursor.description is None:
                cursor.nextset()
                
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
        return jsonify({"error": str(e)}),500