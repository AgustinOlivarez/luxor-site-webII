  const toggle = document.getElementById("menuToggle");
  const menu = document.getElementById("menu");

  // Abrir / cerrar con botón
  toggle.addEventListener("click", () => {
    menu.classList.toggle("active");
  });

  // Cerrar al hacer click en un link
  document.querySelectorAll(".menu a").forEach(link => {
    link.addEventListener("click", () => {
      menu.classList.remove("active");
    });
  });

  // Cerrar al tocar fuera del menú
  document.addEventListener("click", (e) => {
    if (!menu.contains(e.target) && !toggle.contains(e.target)) {
      menu.classList.remove("active");
    }
  });