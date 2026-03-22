from flask import Blueprint, request, jsonify
from controlador.API_varias import SESIONES  # <-- reutilizamos la memoria
from conexion_BD.db import get_connection_dynamic


actuaImei_bp = Blueprint("actuaImei", __name__)


@actuaImei_bp.route('/actualizar-imei', methods=['POST'])
def actualizar():
    try:
        data = request.json
        session_id = data['session_id']

        sesion = SESIONES.get(session_id)

        if not sesion:
            return jsonify({"error":"Sesión Inválida"}) ,401

        database = data['database']
        patente  = data.get('patenteFinal','')
        columna = data.get('columna','')
        parametro = data.get('parametro','')
        
        with get_connection_dynamic(sesion['server'],sesion['user'],sesion['password'],database) as conn:
            cursor = conn.cursor()

            query ="""
                    declare 
                    @patente varchar(20) = ?, -- unidad que vamos a afectar

                    -- Nombre de la columna a modificar
                    @columna varchar(20) = ?,
                    -- Variable que ingresa
                    @param varchar(max) = ?  


                    if @param is not null and replace(@param,' ','') <> ''
                    begin

                        if @columna = 'MOV_IDGPS'
                        begin
                                if exists (select * from moviles where MOV_IDGPS = @param and MOV_CODIGO <> @patente)
                                begin
                                    select 'Error: Dispositivo Ya existe - ingrese otro'
                                end
                                else
                                begin
                                        update moviles 
                                        set MOV_IDGPS = @param
                                        where mov_codigo = @patente
                                        select 'Exito: se cambia equipo GPS exitosamente'
                                        -- esto lo debo eliminar despues
                                end
                        end
                        else
                        begin
                                -- se modifica unicamente el mov patente
                                if @columna = 'MOV_PATENTE'
                                    begin
                                        update moviles 
                                        set MOV_PATENTE = @param
                                        where mov_codigo = @patente

                                        select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                            
                                    end
                                    -- se modifica unicamente el mov iddmr o satelital
                                if @columna = 'MOV_IDDMR'
                                begin
                                        update moviles 
                                        set MOV_IDDMR = @param
                                        where mov_codigo = @patente
                                            
                                        select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                            

                                end
                                -- se modifica unicamente el mov nombre
                                if @columna = 'MOV_NOMBRE'
                                begin
                                    update moviles 
                                    set MOV_NOMBRE = @param
                                    where mov_codigo = @patente
                                        
                                    select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                        
                                        
                                end
                                -- se modifica unicamente el mov foto
                                if @columna = 'MOV_FOTO'
                                begin
                                    update moviles 
                                    set MOV_FOTO = @param
                                    where mov_codigo = @patente
                                        
                                    select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                        
                                end
                                -- se modifica unicamente el mov velmax
                                if @columna = 'MOV_VELMAX'
                                begin
                                    update moviles 
                                    set MOV_VELMAX = @param
                                    where mov_codigo = @patente
                                        
                                    select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                        
                                end
                                -- se modifica unicamente el mov grupo1
                                if @columna = 'MOV_GRUPO1'
                                begin
                                    update moviles 
                                    set MOV_GRUPO1 = @param
                                    where mov_codigo = @patente
                                        
                                    select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                        
                                end
                                -- se modifica unicamente el mov grupo2
                                if @columna = 'MOV_GRUPO2'
                                begin
                                    update moviles 
                                    set MOV_GRUPO2 = @param
                                    where mov_codigo = @patente
                                        
                                    select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                        
                                end
                                -- se modifica unicamente el mov grupo3
                                if @columna = 'MOV_GRUPO3'
                                begin
                                    update moviles 
                                    set MOV_GRUPO3 = @param
                                    where mov_codigo = @patente
                                        
                                    select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                        
                                end
                                -- se modifica unicamente el mov grupo4
                                if @columna = 'MOV_GRUPO4'
                                begin
                                    update moviles 
                                    set MOV_GRUPO4 = @param
                                    where mov_codigo = @patente
                                        
                                    select 'Exito: se modifica la columna: ' +@columna + ' exitosamente'
                                                        
                                end


                        end
                    end

                    else
                        begin
                                select 'Error: parametro vacio'
                        end




            
            """

            params = (patente,columna,parametro)
            cursor.execute(query,params)
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