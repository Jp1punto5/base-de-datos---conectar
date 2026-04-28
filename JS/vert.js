let map;
let markers = [];
let markerSeleccionado = null;
let infoWindow;   // mapa principal



// 🔥 CARGA INICIAL
document.addEventListener("DOMContentLoaded", () => {

    configurarPlaceholders(); // 🔥 AQUÍ SE ACTIVA

    cargarDatos();
    hacerModalMovible();
});



//--------- Volver al Home -------------
document.getElementById("id_home").onclick = function() {
    window.location.href = "home.html";
}

// ---------------- PARAMETROS RECIBIDOS ----------------

const params = new URLSearchParams(window.location.search);

const tabla = params.get('tabla');
const session_id = params.get('session_id');
const database = params.get('database');

// almacenamos los datos en localStore de la pagina actual para reutilizar la navecación entre modulos
    if (session_id && database) {
        localStorage.setItem('session_id', session_id);
        localStorage.setItem('database', database);
    }

document.getElementById('titulo').innerText = "Tabla: " + tabla.toUpperCase();


// --- mostramos en consola los datos recibidos previamente ---------
    if(session_id && database)
    {
        console.log("id de la sesion:",session_id);
        console.log("base de datos: ",database);
    }





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

// esta funcion permite seleccionar la fila para mostrar sus datos en el mapa
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

    // Solo en caso de que se necesite realmente, descomentar

    // if (tabla.toLowerCase() === "reportabilidad") {
    //     if (!columnas.includes("Dirección")) {
    //         columnas.push("Dirección");
    //     }
    // }

    columnas.forEach((col) => {
        const th = document.createElement('th');

        // Cambiar el nombre de la columna si es "id_tipointegracion"
        if (col.toLowerCase() === "id_tipointegracion") {
            col = "Nombre Integración"; // Cambiar el nombre de la columna
        }

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

            } else if (col.toLowerCase() === "id_tipointegracion") 
            {
                console.log("llegamos a la columna Nombre Integración");
                console.log("row[col] =", row[col]);
                // Array con los datos de las integraciones
                const integraciones = 
                [
                    {id : "41", nombre : "API - Samtech"},
                    {id:"47", nombre : "API - GPSChile - (GPS)"},
                    {id:"98", nombre : "API - Lomas Bayas"},
                    {id:"107" , nombre:"API - OWL Caserones"},
                    {id: "110", nombre: "API - Tracktec MEL Escondida"},
                    {id:"111", nombre : "API - OWL Codelco (El Teniente)"},
                    {id:"130", nombre:"API - SKYNAV PELAMBRES"},
                    {id:"95", nombre: "API - SKYNAV CENTINELA"},
                    {id:"113", nombre:"API - SKYNAV ANTUCOYA"},
                    {id:"141",nombre:"API - SKYNAV CyG"}
                ]
                 // Buscar el nombre de la integración usando el ID
                 const integracion = integraciones.find(integracion => String(integracion.id) === String(row[col]));
                  // Si encontramos el ID, asignamos el nombre, si no, mostramos el ID
                 td.innerText = integracion ? integracion.nombre : row[col];
            }  
        
             else if (col === "Dirección")
            {
                    const latt = row["Latitud"] || row["latitud"];
                    const lonn = row["Longitud"] || row["longitud"];
                if (latt && lonn) 
                    {
                        obtenerDireccion(latt, lonn).then(direccion => {
                        td.innerText = direccion;
                        }).catch(() => {
                            td.innerText = "Sin dirección";
                        });
                } 
                else 
                {
                    td.innerText = "Sin coordenadas";
                }
            }
        
             
            else 
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
    const filtro2 = document.getElementById('filtro2'); // aqui obtengo el INPUT
    let filtropatente = filtro2.value.trim(); // aqui asigno el valor ingresado por el usuario.
    // console.log("valor:", filtropatente);
    // console.log("length:", filtropatente.length);
    // console.log("chars:", filtropatente.split(""));
    // console.log("includes -:", filtropatente.includes("-"));
   
        if (filtropatente.length === 6 && !filtropatente.includes("-") || filtropatente.length === 6)
        {
            filtropatente = filtropatente.slice(0,4)+"-"+filtropatente.slice(4,6);
        }

    // creamos variable que contendra el listado de patentes si existen
    const listPatente = document.getElementById("inputPatentes");

    const textareaValue = listPatente.value.trim();

    let patentes = [];
    let errorPatente = [];
    let seen = new Set();
    
    if (textareaValue) {
        patentes = textareaValue
            .split(/[\n,\/]+/) 
            .reduce((acc, p) => {
                // lo que hace el trim es eliminar espacios de inicio y los de fin NO los del medio
                const limpia = p.trim().replace(/\s+/g,'').replace(/[^a-zA-Z0-9]/g, '');
                if (!limpia) return acc;
                // a continuación verificamos primero si el dato entregado es o no un VIN | OJO no es un validar vin, solo detecta un caracter de largo 7 u 8 sin guion y lo deja entrar
                if (!limpia.includes("-") && [7, 8].includes(limpia.length))
                {
                    seen.add(limpia);
                    acc.push(limpia);
                    console.log("dato: " + limpia);
                }
                else
                {
                    const validada = validarPatente(limpia);
                    if (validada && !seen.has(validada)) {
                        seen.add(validada);
                        acc.push(validada);
                    }else
                    {
                        errorPatente.push(limpia);
                    }
                }

                return acc;
            }, []);
        

        

    }


    if (filtropatente || patentes.length >0)
    {
        console.log("dato del filtro2: "+ filtropatente);
            if (!filtropatente.includes("-") && [7, 8].includes(filtropatente.length))
            {
                patentes.push(filtropatente);
            } else if (filtropatente)
            {
                
                // se crea una variable para validar la patente del filtro2
                const validarFiltro2 = validarPatente(filtropatente);
                // si la patente es valida se asigna al array que se envía a la API
                if (validarFiltro2)
                {
                    patentes.push(validarFiltro2);
                }
                else // si la patente no es valida, se agrega al array de errores
                {
                    errorPatente.push(filtropatente);
                }
                 
            }
        // aqui lo que hacemos, es limpiar y al mismo tiempo asignar nuevos valores a la variable que sera enviada para consumir la API /tabla
        filtropatente = patentes;
    }

     // aqui validamos si existen datos en el array errorPatente que contendra las unidades mal ingresadas
    if (errorPatente.length > 0) 
    {
        mostrarAlerta("No se encontraron las siguientes unidades:<ul><li>" + errorPatente.join("</li><li>") + "</li></ul>", "error");
    }
   // aqui limpiamos los campos para eliminar los datos ya buscados
    filtro2.value = "";
    listPatente.value = "";
  
    console.log("datos que se quieren enviar como patente: " + filtropatente);
    const limite = Number(document.getElementById('limite').value) || 10;

    document.getElementById('estado').innerText = "⏳ Cargando...";
    console.log("Tabla:" + tabla);


    // 🔥 si no hay muchas patentes, usa tu lógica normal
    if (!Array.isArray(filtropatente) || filtropatente.length <= 2000) {

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
            .then(response => manejarRespuesta(response));

    } else {

        // 🔥 dividir en bloques
        const dividirArray = (array, tamaño = 2000) => {
            const resultado = [];
            for (let i = 0; i < array.length; i += tamaño) {
                resultado.push(array.slice(i, i + tamaño));
            }
            return resultado;
        };

        const chunks = dividirArray(filtropatente, 2000);
        const MAX_CONCURRENTE = 4; // este es el maximo de solicitudes simultaneas a la API

        let datosFinales = [];
        let columnasGlobalTemp = null;

        const procesarChunks = async () => {
            for (let i = 0; i < chunks.length; i += MAX_CONCURRENTE) {

                const grupo = chunks.slice(i, i + MAX_CONCURRENTE);

                const promesas = grupo.map(chunk => {
                    return fetch('http://127.0.0.1:5000/tabla', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            session_id,
                            database,
                            tabla,
                            filtro1,
                            filtropatente: chunk,
                            limite: chunk.length // este dato realmente no es utilizado en el backend, ya que en  la API se toma como limite el largo de "filtroPatente"
                        })
                    }).then(res => res.json());
                });

                const respuestas = await Promise.all(promesas);

                respuestas.forEach(response => {
                    if (!response.error) {
                        datosFinales.push(...response.data);

                        if (!columnasGlobalTemp) {
                            columnasGlobalTemp = response.columnas;
                        }
                    }
                });
            }

            manejarRespuesta({
                data: datosFinales,
                columnas: columnasGlobalTemp
            });
        };

        procesarChunks();
    }
}


    // se crea función para dividir y crear bloques de datos
    function dividirArray(array, tamaño = 2000) {
        const resultado = [];
        for (let i = 0; i < array.length; i += tamaño) {
            resultado.push(array.slice(i, i + tamaño));
        }
        return resultado;
    }

// función para manejar respuesta de la  API Tabla

    function manejarRespuesta(response) {

        if (response.error) {
            document.getElementById('estado').innerText = "❌ " + response.error;
            return;
        }

        const data = response.data;
        const columnas = response.columnas;

        console.log(columnas);
        console.log(data);

        document.getElementById('estado').innerText = `✅ ${data.length} registros`;

        datosGlobal = data;
        columnasGlobal = columnas;

        renderTabla(data, columnas);

        const layout = document.querySelector(".layout-mapa");
        const mapaContainer = document.querySelector(".mapa-container");

        if(data.length !== limite && data.length > 0) {
            if (data.length === 1) {
                mostrarAlerta(data.length+" Vehículo encontrado","success");
            } else {
                mostrarAlerta(data.length+" Vehículos encontrados","success");
            }
        }

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