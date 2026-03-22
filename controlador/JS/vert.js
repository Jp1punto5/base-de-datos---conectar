let map;
let markers = [];
let markerSeleccionado = null;
let infoWindow;   // mapa principal

// ---------------- PARAMETROS ----------------

const params = new URLSearchParams(window.location.search);

const tabla = params.get('tabla');
const session_id = params.get('session_id');
const database = params.get('database');

document.getElementById('titulo').innerText = "Tabla: " + tabla.toUpperCase();


// 🔥 PLACEHOLDER DINÁMICO
function configurarPlaceholders() {

    const filtro1 = document.getElementById("filtro1");
    const filtro2 = document.getElementById("filtro2");

    if (filtro1) {
        const configTabla = {
            MOVILES_EQUIPAMIENTO: "Buscar por equipamiento...",
            reportabilidad: "Buscar por chasis...",
            MOVILES: "Buscar por Solución o Fecha Instalación GPS"
        };

        filtro1.placeholder = configTabla[tabla] || "Filtro general...";
    }

    if (filtro2) {
        filtro2.placeholder = "Buscar por patente...";
    }
}

// ---------------- MAPA ----------------

function initMapa() {
    map = new google.maps.Map(document.getElementById("mapa"), {
        center: { lat: -33.45, lng: -70.66 },
        zoom: 6
    });

    infoWindow = new google.maps.InfoWindow();

    // 🔥 ZOOM DINÁMICO DEL POPUP
    map.addListener("zoom_changed", () => {
        const zoom = map.getZoom();
        const popup = document.querySelector(".popup-gps");

        if (!popup) return;

        if (zoom >= 15) popup.style.fontSize = "16px";
        else if (zoom >= 12) popup.style.fontSize = "14px";
        else popup.style.fontSize = "12px";
    });
}

function limpiarMarkers() {
    markers.forEach(m => m.setMap(null));
    markers = [];
}

function agregarMarkers(data) {
    limpiarMarkers();

    data.forEach((row, index) => {

        const url = row["Ubicación"];
        if (!url || !url.includes("maps.google")) return;

        const coords = url.split("q=")[1].split(",");
        const lat = parseFloat(coords[0]);
        const lng = parseFloat(coords[1]);

        if (isNaN(lat) || isNaN(lng)) return;

        const marker = new google.maps.Marker({
            position: { lat, lng },
            map,
            title: row["Patente"]
        });

        const estado = row["Estado GPS"] || "";
        const claseEstado = estado.includes("ONLINE") ? "estado-online" : "estado-offline";

        const contenido = `
            <div class="popup-gps pro">

                <div class="popup-header">
                    <i class="fa-solid fa-car"></i>
                    <span>${row["Patente"] || "Sin patente"}</span>
                </div>

                <div class="popup-body">

                    <div class="item">
                        <i class="fa-solid fa-calendar"></i>
                        <div>
                            <small>Últ. Reporte</small>
                            <span>${row["Últ. Reporte"]}</span>
                        </div>
                    </div>

                    <div class="item">
                        <i class="fa-solid fa-signal"></i>
                        <div>
                            <small>Estado</small>
                            <span class="${claseEstado}">${estado}</span>
                        </div>
                    </div>

                    <div class="item">
                        <i class="fa-solid fa-gauge"></i>
                        <div>
                            <small>Velocidad</small>
                            <span>${row["Velocidad"]}</span>
                        </div>
                    </div>

                    <div class="item">
                        <i class="fa-solid fa-brain"></i>
                        <div>
                            <small>Evento</small>
                            <span>${row["N° | Evento"]}</span>
                        </div>
                    </div>

                </div>
            </div>
        `;

        marker.addListener("click", () => {

            resaltarFila(index);

            map.setZoom(15);
            map.panTo(marker.getPosition());

            infoWindow.setContent(contenido);
            infoWindow.open(map, marker);
        });

        markers.push(marker);
    });
}

function centrarMapa() {
    if (markers.length === 0) return;

    const bounds = new google.maps.LatLngBounds();
    markers.forEach(m => bounds.extend(m.getPosition()));
    map.fitBounds(bounds);
}

function resaltarMarker(index) {
    if (markerSeleccionado) {
        markerSeleccionado.setAnimation(null);
    }

    const marker = markers[index];
    if (!marker) return;

    marker.setAnimation(google.maps.Animation.BOUNCE);
    markerSeleccionado = marker;

    map.setZoom(15);
    map.panTo(marker.getPosition());

    google.maps.event.trigger(marker, "click");
}

function resaltarFila(index) {
    const filas = document.querySelectorAll("#tabla tr");
    filas.forEach(f => f.classList.remove("fila-activa"));

    const fila = filas[index + 1];
    if (fila) fila.classList.add("fila-activa");
}



// ---------------- TABLA ----------------

let datosGlobal = [];
let columnasGlobal = [];
let ordenAsc = true;
let columnaActiva = null;

function renderTabla(data, columnas) {
    const table = document.getElementById('tabla');
    table.innerHTML = '';

    const header = document.createElement('tr');

    columnas.forEach((col) => {
        const th = document.createElement('th');

        let indicador = "";
        if (col === columnaActiva) {
            indicador = ordenAsc ? " ↑" : " ↓";
        }

        th.innerText = col + indicador;
        th.onclick = () => ordenarPor(col);

        header.appendChild(th);
    });

    table.appendChild(header);

    data.forEach((row, index) => {
        const tr = document.createElement('tr');

        tr.onclick = () => {
            resaltarMarker(index);

            document.querySelectorAll("#tabla tr").forEach(r => r.classList.remove("fila-activa"));
            tr.classList.add("fila-activa");
            // con este if logro activar el MODAL unicamente cuando estemos en el modulo correcto.
            if (tabla === "MOVILES")
            {
                abrirModal(row); // 🔥 AQUÍ VA EL MODAL
            }
            
         };

        columnas.forEach(col => {
            const td = document.createElement('td');
            //------------vamos a verificar si es la columna fecha_insertado para transformar el resultado. esto viene de la tabla moviles_equipamiento
            if (col.toLowerCase() === "fecha_insertado") {

                const fecha = new Date(row[col]);

                const dia = String(fecha.getDate()).padStart(2, '0');
                const mes = String(fecha.getMonth() + 1).padStart(2, '0');
                const anio = fecha.getFullYear();

                const horas = String(fecha.getHours()).padStart(2, '0');
                const minutos = String(fecha.getMinutes()).padStart(2, '0');

                td.innerText = `${dia}/${mes}/${anio} ${horas}:${minutos}`;
            }
            // aqui verificamos si existe la columna ubicacion que viene del inner join de la reportabilidad
            else  if (col === "Ubicación" && row[col]) {

                const link = document.createElement("a");
                link.href = row[col];
                link.target = "_blank";
                link.innerText = "Ver ubicación 📍";

                td.appendChild(link);

            } else 
             {
                    td.innerText = row[col];
             }

            tr.appendChild(td); // 🔥 ESTA LÍNEA FALTABA
        });

        table.appendChild(tr);
    });

    setTimeout(() => {
        document.getElementById("scrollTopInner").style.width =
            document.getElementById("tabla").scrollWidth + "px";
    }, 100);
}

function ordenarPor(columna) {
    ordenAsc = (columnaActiva === columna) ? !ordenAsc : true;
    columnaActiva = columna;

    datosGlobal.sort((a, b) => {
        if (a[columna] < b[columna]) return ordenAsc ? -1 : 1;
        if (a[columna] > b[columna]) return ordenAsc ? 1 : -1;
        return 0;
    });

    renderTabla(datosGlobal, columnasGlobal);
}



// --------- validar patente -------------

function validarPatente(patente) {
    let limpia = patente.replace(/[^a-zA-Z0-9]/g, "").toUpperCase();

    const regexNueva = /^[A-Z]{4}[0-9]{2}$/;
    const regexAntigua = /^[A-Z]{2}[0-9]{4}$/;

    if (regexNueva.test(limpia)) {
        return `${limpia.slice(0,4)}-${limpia.slice(4,6)}`;
    } 
    else if (regexAntigua.test(limpia)) {
        return `${limpia.slice(0,2)}-${limpia.slice(2,6)}`;
    } 
    else {
        console.log("Formato de patente inválido");
        return null;
    }
}



// ---------------- API ----------------

function cargarDatos() {

    if (!session_id || !database) {
        document.getElementById('estado').innerText = "❌ Sesión inválida";
        return;
    }

    const filtro1 = document.getElementById('filtro1').value;
    const filtro2 = document.getElementById('filtro2').value;
    let filtropatente = validarPatente(filtro2);

    const limite = document.getElementById('limite').value || 10;

    document.getElementById('estado').innerText = "⏳ Cargando...";

    fetch('http://127.0.0.1:5000/tabla', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id,
            database,
            tabla,
            filtro1,
            filtropatente,
            limite
        })
    })
    .then(res => res.json())
    .then(response => {

        if (response.error) {
            document.getElementById('estado').innerText = "❌ " + response.error;
            return;
        }

        const data = response.data;
        const columnas = response.columnas;
        console.log(columnas);
        document.getElementById('estado').innerText = `✅ ${data.length} registros`;

        datosGlobal = data;
        columnasGlobal = columnas;

        renderTabla(data, columnas);

        const layout = document.querySelector(".layout-mapa");
        const mapaContainer = document.querySelector(".mapa-container");

        if (tabla.toLowerCase() === "reportabilidad") {

            mapaContainer.classList.remove("oculto");
            layout.classList.remove("sin-mapa");

            if (!map) initMapa();

            agregarMarkers(data);
            centrarMapa();

            setTimeout(() => {
                google.maps.event.trigger(map, "resize");
                centrarMapa();
            }, 200);

        } else {

            mapaContainer.classList.add("oculto");
            layout.classList.add("sin-mapa");

            limpiarMarkers();
        }
    });
}

// ---------------- INIT ----------------

document.querySelector(".mapa-container").classList.add("oculto");
document.querySelector(".layout-mapa").classList.add("sin-mapa");

window.initMapa = function () {
    map = new google.maps.Map(document.getElementById("mapa"), {
        center: { lat: -33.45, lng: -70.66 },
        zoom: 6
    });

    infoWindow = new google.maps.InfoWindow();
};

// scroll sync
const topScroll = document.getElementById("scrollTop");
const bottomScroll = document.getElementById("scrollBottom");

topScroll.addEventListener("scroll", () => {
    bottomScroll.scrollLeft = topScroll.scrollLeft;
});

bottomScroll.addEventListener("scroll", () => {
    topScroll.scrollLeft = bottomScroll.scrollLeft;
});

// 🔥 CARGA INICIAL
document.addEventListener("DOMContentLoaded", () => {

    configurarPlaceholders(); // 🔥 AQUÍ SE ACTIVA

    cargarDatos();
    hacerModalMovible();
});



function filtrarTabla() {
    const input = document.getElementById("busquedaTabla");
    const filtro = input.value.toLowerCase();

    const filas = document.querySelectorAll("#tabla tr");

    filas.forEach((fila, index) => {

        // saltar header
        if (index === 0) return;

        const textoFila = fila.innerText.toLowerCase();

        if (textoFila.includes(filtro)) {
            fila.style.display = "";
        } else {
            fila.style.display = "none";
        }
    });
}

// ---------- este componente se activa para mostrar informacion del largo permitido en un INPUT ---------------
document.querySelectorAll('input[maxlength]').forEach(input => {

    const popup = document.createElement('div');
    popup.classList.add('input-popup');
    popup.innerText = `Máximo ${input.maxLength} caracteres`;
    document.body.appendChild(popup);

    input.addEventListener('input', () => {
        if (input.value.length >= input.maxLength) { // llega al límite
            const rect = input.getBoundingClientRect();
            popup.style.top = rect.top - 30 + window.scrollY + 'px';
            popup.style.left = rect.left + window.scrollX + 'px';
            popup.classList.add('show');

            clearTimeout(popup.hideTimeout);
            popup.hideTimeout = setTimeout(() => {
                popup.classList.remove('show');
            }, 1500);
        }
    });
});