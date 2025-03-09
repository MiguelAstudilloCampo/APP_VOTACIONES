document.addEventListener("DOMContentLoaded", function () {
    const opciones = document.querySelectorAll(".OP");

    opciones.forEach(opcion => {
        opcion.addEventListener("click", function () {
            opciones.forEach(op => op.classList.remove("selected"));

            this.classList.add("selected");

            console.log("Votaste por:", this.dataset.candidate);
        });
    });
});
