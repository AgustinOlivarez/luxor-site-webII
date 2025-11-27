document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contacto-form");
    const btn = document.getElementById("btn-enviar");
    const spinner = document.getElementById("btn-spinner");


    form.addEventListener("submit", function (e) {
        let errores = [];
        btn.setAttribute("disabled", "true");
        btn.classList.add("disabled");

        spinner.style.display = "inline-block";

        const nombre = form.nombre.value.trim();
        const email = form.email.value.trim();
        const asunto = form.asunto.value.trim();
        const mensaje = form.mensaje.value.trim();

        if (nombre.length < 3) errores.push("El nombre es muy corto.");
        if (!email.includes("@")) errores.push("Email inválido.");
        if (asunto.length < 3) errores.push("El asunto es muy corto.");
        if (mensaje.length < 5) errores.push("El mensaje es demasiado breve.");

        if (errores.length > 0) {
            e.preventDefault();
            alert(errores.join("\n"));
        }
    });
});

    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }
    }, 3000);