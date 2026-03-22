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
        document.getElementById('edit_patente').value = row.MOV_PATENTE;
        document.getElementById('edit_dispositivo').value = row.MOV_IDGPS;
        document.getElementById('edit_nombre').value = row.MOV_NOMBRE;
        document.getElementById('edit_iddmr').value = row.MOV_IDDMR;
        document.getElementById('edit_foto').value = row.MOV_FOTO;
        document.getElementById('edit_velocidad').value = row.MOV_VELMAX;
        document.getElementById('edit_grupo1').value = row.MOV_GRUPO1;
        document.getElementById('edit_grupo2').value = row.MOV_GRUPO2;
        document.getElementById('edit_grupo3').value = row.MOV_GRUPO3;
        document.getElementById('edit_grupo4').value = row.MOV_GRUPO4;

        resetInputs();

        setTimeout(() => {
            if (!mapModal) {
                cargarMapaInicial();
                actualizarPosicion();
            }

            google.maps.event.trigger(mapModal, "resize");
            mapModal.setCenter({ lat: -33.45, lng: -70.66 });
            mapModal.setZoom(13);

        }, 300);
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
                alert("No reporta");
                return;
            }

            const data = response.data;
            let estado_ing = "";
            console.log("estado ignicion:",data.Mopo_Estado_Ignicion);
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
                                <i class="fa-solid fa-gauge"></i>
                                <div>
                                    <small>Estado Ignición</small>
                                    <span class="evento">${estado_ing}</span>
                                </div>
                            </div>  

                        </div>
                    </div>
                `
            });

            infoWindowModal.open(mapModal, marker);

        });
    }

    function guardarCambios() {
        patente = document.getElementById("edit_codigo").innerText;

        //variables del MODAL
        const m_patente = document.getElementById("edit_patente").value;
        const m_idgps   = document.getElementById("edit_dispositivo").value;
        const m_nombre  = document.getElementById("edit_nombre").value;
        const m_sateli  = document.getElementById("edit_iddmr").value;
        const m_foto    = document.getElementById("edit_foto").value;
        const m_vel     = document.getElementById("edit_velocidad").value;
        const m_grupo1  = document.getElementById("edit_grupo1").value;
        const m_grupo2  = document.getElementById("edit_grupo2").value;
        const m_grupo3  = document.getElementById("edit_grupo3").value;
        const m_grupo4  = document.getElementById("edit_grupo4").value;
        


        console.log(patente,m_patente);
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

    // 🔥 EXPONER SOLO LO NECESARIO
    window.abrirModal = abrirModal;
    window.cerrarModal = cerrarModal;
    window.habilitarCampo = habilitarCampo;
    window.actualizarPosicion = actualizarPosicion;
    window.hacerModalMovible = hacerModalMovible;
    window.guardarCambios = guardarCambios;

})();