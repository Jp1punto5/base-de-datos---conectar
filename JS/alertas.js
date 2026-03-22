function mostrarAlerta(mensaje, tipo = "info") {

    const alerta = document.createElement("div");
    alerta.classList.add("alerta", tipo);

    alerta.innerHTML = `
        <span>${mensaje}</span>
        <button class="cerrar">&times;</button>
    `;

    document.body.appendChild(alerta);

    // 🔥 Posicionar correctamente todas las alertas
    reordenarAlertas();

    // 🔥 Función cerrar
    const cerrar = () => {
        alerta.classList.add("cerrando");

        setTimeout(() => {
            alerta.remove();
            reordenarAlertas(); // 🔥 reacomoda las restantes
        }, 400);
    };

    // Auto cerrar
    setTimeout(cerrar, 4000);

    // Cerrar manual
    alerta.querySelector(".cerrar").addEventListener("click", cerrar);
}

function reordenarAlertas() {
    const alertas = document.querySelectorAll(".alerta");
    let offset = 20; // margen superior inicial

    alertas.forEach(alerta => {
        alerta.style.top = `${offset}px`;
        offset += alerta.offsetHeight + 10; // 10px de espacio entre alertas
    });
}