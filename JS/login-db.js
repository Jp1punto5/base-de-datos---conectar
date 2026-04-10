//----------- Aqui estan las funciones que conectan la base de datos y redireccionan a la otra Url



function conectarBD() {
    const database = document.getElementById('databases').value;

    localStorage.setItem('database', database);

    document.getElementById('tablas').style.display = 'block';
}

//---------------------  Funcion Redirección -------------------

function abrirTabla(tabla) {
  

    const session_id = localStorage.getItem('session_id');
    const database = localStorage.getItem('database');

    const url = `vertabla.html?tabla=${tabla}&database=${database}&session_id=${session_id}`;

    window.location.assign(url);
}


// 🔥 Paso 1: LOGIN
function conectar() {
    const server = document.getElementById('server').value;
    if(!server)
    {
        mostrarAlerta("Se debe seleccionar una Base de datos","warning");
    }
    const user = document.getElementById('user').value;
    const password = document.getElementById('password').value;

    document.getElementById('estado').innerText = "⏳ Conectando...";

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ server, user, password })
    })
    .then(res => res.json())
    .then(data => {

        if (data.error) {
            document.getElementById('estado').innerText = "❌ Error: " + data.error;
            return;
        }

        localStorage.setItem('session_id', data.session_id);

        document.getElementById('estado').innerText = "✅ Conectado";

        cargarBases();
    })
    .catch(err => {
        document.getElementById('estado').innerText = "❌ Error conexión";
        console.error(err);
        const tablas = document.getElementById('tablas');
        if (tablas.style.display === "block")
    {
        tablas.style.display = "none";
    }
    });
}


// 🔥 Paso 2: listar BD
function cargarBases() {
    const session_id = localStorage.getItem('session_id');

    fetch('http://127.0.0.1:5000/listar-bd', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id })
    })
    .then(res => res.json())
    .then(data => {

        const select = document.getElementById('databases');
        select.innerHTML = '';

        data.forEach(db => {
            const option = document.createElement('option');
            option.value = db;
            option.text = db;
            select.appendChild(option);
        });

        select.disabled = false;
        document.getElementById('btnConectarBD').disabled = false;
    });
}

