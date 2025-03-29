let teclaodvisible = false;
function mostrarTeclado() {
    teclado = document.getElementById("math-panel");
    teclado.style.display = "flex";
    setTimeout(() => {
        teclado.style.bottom = "0px";
        teclado.style.opacity = "1";
        teclado.style.transform = "scale(1)";
    }, 50);

    teclaodvisible = true;
}

function ocultarTeclado() {
    teclado = document.getElementById("math-panel");
    teclado.style.bottom = "-100px";
    teclado.style.opacity = "0";
    teclado.style.transform = "scale(0.8)";
    setTimeout(() => {
        teclado.style.display = "none";
    }, 500);
    teclaodvisible = false;
}

document.addEventListener('click', function (e) {
    if (!(e.target.closest('#math-panel') || e.target.closest('#math-field') || e.target.closest(".sugerencias"))) {
        ocultarTeclado();
    }
    else if (!e.target.closest(".sugerencias")) {
        mostrarTeclado();
    }
});