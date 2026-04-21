(function () {

    let mapModal;
    let marker;
    let infoWindowModal;
    // variable GLOBAL
    let patente; 


    function abrirModal(row) {

        if (window.infoWindowMain) {
            window.infoWindowMain.close();
        }

        const modal = document.getElementById('modalEditar');
        modal.style.display = 'block';

        /* 🔥 RESET SCROLL */
        const scrollContainer = modal.querySelector('.modal-form-scroll');
        if (scrollContainer) {
            scrollContainer.scrollTop = 0;
        }

        document.getElementById('edit_codigo').innerText = row.MOV_CODIGO;
        if (!row.MOV_SIMCARD)
        {
            document.getElementById("edit_simcard").innerText = "Sin datos";
        }
        else
        {
            document.getElementById("edit_simcard").innerText = row.MOV_SIMCARD;
        }
        
        setInput('edit_patente', row.MOV_PATENTE);
        setInput('edit_dispositivo', row.MOV_IDGPS);
        setInput('edit_nombre', row.MOV_NOMBRE);
        setInput('edit_iddmr', row.MOV_IDDMR);
        setInput('edit_foto', row.MOV_FOTO);
        setInput('edit_velocidad', row.MOV_VELMAX);
        setInput('edit_grupo1', row.MOV_GRUPO1);
        setInput('edit_grupo2', row.MOV_GRUPO2);
        setInput('edit_grupo3', row.MOV_GRUPO3);
        setInput('edit_grupo4', row.MOV_GRUPO4);

        resetInputs();

        setTimeout(() => {
            if (!mapModal) {
                cargarMapaInicial();
               
            }

            actualizarPosicion(); // siempre se ejecuta

            google.maps.event.trigger(mapModal, "resize");
            mapModal.setCenter({ lat: -33.45, lng: -70.66 });
            mapModal.setZoom(13);

        }, 300);
    }

    // la siguiente funcion permite asignacion mas rapida a un input
    function setInput(id, valor) {
        const input = document.getElementById(id);
        input.value = valor;
        input.dataset.original = valor;
    }

    function cargarMapaInicial() {
        mapModal = new google.maps.Map(document.getElementById("map"), {
            center: { lat: -33.45, lng: -70.66 },
            zoom: 12
        });
    }

    function resetInputs() {
        document.querySelectorAll('#modalEditar input')
            .forEach(i => i.disabled = true);
    }

    function cerrarModal() {
        const modal = document.getElementById('modalEditar');
        modal.style.display = 'none';

        /* 🔥 RESET SCROLL TAMBIÉN AL CERRAR */
        const scrollContainer = modal.querySelector('.modal-form-scroll');
        if (scrollContainer) {
            scrollContainer.scrollTop = 0;
        }

        resetInputs();
    }

    function habilitarCampo(id) {
        document.getElementById(id).disabled = false;
    }

    function actualizarPosicion() {

        patente = document.getElementById("edit_codigo").innerText;

        fetch('http://127.0.0.1:5000/estado-dispositivo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id, database, patente })
        })
        .then(res => res.json())
        .then(response => {

            if (!response.reporta) {
                mostrarAlerta("Vehículo:"+patente+" nunca ha reportado","error");
                return;
            }

            const data = response.data;
            let estado_ing = "";
            // con este bloque if podemos identificar si la antena se encuentra valida o no
            let antena = data.mopo_estado;
            if (antena === "A")
            {
                antena = "Valida";
            }
            else 
            {
                antena = "Invalida";
            }
            console.log("estado ignicion:",data.Mopo_Estado_Ignicion);
            console.log("estado antena:",data.mopo_estado);
            if (data.Mopo_Estado_Ignicion)
            {
                estado_ing = "Encendido";
            }
            else{
                estado_ing = "apagado";
            }
            const pos = {
                lat: parseFloat(data.mopo_lat),
                lng: parseFloat(data.mopo_lon)
            };

            mapModal.setCenter(pos);
            mapModal.setZoom(16);

            if (marker) marker.setMap(null);

            marker = new google.maps.Marker({
                position: pos,
                map: mapModal,
                animation: google.maps.Animation.DROP,
                icon: {
                    url: "https://maps.google.com/mapfiles/ms/icons/green-dot.png"
                }
            });

            if (infoWindowModal) infoWindowModal.close();

            infoWindowModal = new google.maps.InfoWindow({
                content: `
                    <div class="popup-gps pro">

                        <div class="popup-header">
                            <i class="fa-solid fa-car"></i>
                            <span>${patente || "Sin patente"}</span>
                        </div>
                        </br>
                        <div class="popup-body">

                            <div class="item">
                                <i class="fa-solid fa-calendar"></i>
                                <div>
                                    <small>Últ. Reporte</small>
                                    <span>${data.mopo_fechahora}</span>
                                </div>
                            </div>

                            <div class="item">
                                <i class="fa-solid fa-gauge"></i>
                                <div>
                                    <small>Velocidad</small>
                                    <span class="velocidad">${data.mopo_vel}</span>
                                </div>
                            </div>   
                           
                            <div class="item">
                                <i class="fa-solid fa-key"></i>
                                <div>
                                    <small>Estado Ignición</small>
                                    <span class="evento">${estado_ing}</span>
                                </div>
                            </div>  
                             <div class="item">
                                <i class="fa-solid fa-tower-broadcast"></i>
                                <div>
                                    <small>Estado Antena</small>
                                    <span class="evento">${antena}</span>
                                </div>
                            </div> 

                        </div>
                    </div>
                `
            });

            infoWindowModal.open(mapModal, marker);

        });
    }
    async function guardarCambios() {
        const patente = document.getElementById("edit_codigo").innerText;
        const boton = document.getElementById("btnGuardar");
        const textoOriginal = boton.innerText;

        // 🔹 Detectar todos los inputs dentro del modal que tengan data-columna
        const inputs = document.querySelectorAll('#modalEditar input[data-columna]');
        
        // Filtrar los que realmente van a cambiar
        const inputsACambiar = Array.from(inputs).filter(input => 
            !input.disabled && input.value.toUpperCase() !== input.dataset.original
        );

        if (inputsACambiar.length === 0) {
            mostrarAlerta("No se detectaron cambios", "warning");
            return;
        }

        let i = 0;

        try {
            for (const input of inputsACambiar) {
                i++;

                // 🔹 Contador en el botón
                boton.innerText = `Guardando ${i} de ${inputsACambiar.length}...`;

                const valorActual = input.value;
                const valorMayus = valorActual.toUpperCase();
                const columna = input.dataset.columna;

                try {
                    const response = await fetch("http://127.0.0.1:5000/actualizar-imei", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            session_id: session_id,
                            database: database,
                            patenteFinal: patente,
                            columna: columna,
                            parametro: valorMayus
                        })
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.error || "Error en la API");
                    }

                    // 🔹 Capturar mensaje SQL (éxito o error)
                    if (data.data && data.data[0]) {
                        const mensaje = Object.values(data.data[0])[0];
                        console.log("Mensaje SQL:", mensaje);

                        if (mensaje.startsWith("Error")) {
                            throw new Error(mensaje);
                        } else {

                            // validamos si se cambia la mov_foto o la mov_idgps para disparar el agregar equipamientos
                            if (columna === "MOV_FOTO" || columna === "MOV_IDGPS")
                            {
                                agregarEquipamiento(patente);
                            }
                            mostrarAlerta(mensaje, "success");
                        }
                    }

                    // 🔹 Actualizar input: valor visual + dataset + bloquear
                    input.value = valorMayus;
                    input.dataset.original = valorMayus;
                    input.disabled = true;

                } catch (campoError) {
                    // 🔹 Restaurar el valor original en caso de error
                    input.value = input.dataset.original;
                    input.disabled = true;
                    mostrarAlerta(campoError.message, "error");
                    // detener el loop si quieres, o comentar la siguiente línea para continuar con otros campos
                    break;
                }
            }
        } finally {
            // 🔹 Restaurar texto original del botón
            boton.innerText = textoOriginal;
        }
    }



    // vamos a crear funcion para consumir la API que inserta los equipamientos
    async function agregarEquipamiento(patente) {
        const response = await fetch("http://127.0.0.1:5000/equipamientos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: session_id,   // tu variable global
                database: database,       // tu variable global
                patente: patente
            })
        });

        const data = await response.json();

        // 🔹 Si la API devuelve un error HTTP
        if (!response.ok) {
            mostrarAlerta(data.error || "Error en la API", "error");
            return;
        }

        // 🔹 Tomar directamente el mensaje que retorna la API
        if (data.data && data.data[0]) {
            const mensaje = Object.values(data.data[0])[0];

            // 🔹 Mostrar alerta, sea éxito o error, exactamente como vino
            if (mensaje.toLowerCase().startsWith("exito")) {
                mostrarAlerta(mensaje, "success");
            } else {
                mostrarAlerta(mensaje, "error");
            }
        } else if (data.error) {
            mostrarAlerta(data.error, "error");
        }
    }


    function hacerModalMovible() {
        const modal = document.querySelector(".modal-content");
        const header = document.getElementById("modalHeader");

        let isDragging = false;
        let offsetX = 0;
        let offsetY = 0;

        header.style.cursor = "move";

        header.addEventListener("mousedown", (e) => {
            isDragging = true;
            offsetX = e.clientX - modal.offsetLeft;
            offsetY = e.clientY - modal.offsetTop;
        });

        document.addEventListener("mousemove", (e) => {
            if (!isDragging) return;

            modal.style.position = "absolute";
            modal.style.left = (e.clientX - offsetX) + "px";
            modal.style.top = (e.clientY - offsetY) + "px";
        });

        document.addEventListener("mouseup", () => {
            isDragging = false;
        });
    }


    // cerrar MODAL si se hace click fuera de el
    window.addEventListener('click', function (event) {
    const modal = document.getElementById('modalEditar');

    if (event.target === modal) {
        cerrarModal();
    }
    });

    document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        cerrarModal();
    }
});

    // 🔥 EXPONER SOLO LO NECESARIO
    window.abrirModal = abrirModal;
    window.cerrarModal = cerrarModal;
    window.habilitarCampo = habilitarCampo;
    window.actualizarPosicion = actualizarPosicion;
    window.hacerModalMovible = hacerModalMovible;
    window.guardarCambios = guardarCambios;

})();