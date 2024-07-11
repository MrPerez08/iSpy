document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.querySelector(".menu-toggle");
  const navbar = document.querySelector(".navbar");

  menuToggle.addEventListener("click", function () {
    menuToggle.classList.toggle("active");
    navbar.classList.toggle("active");
  });

  document.addEventListener("click", function (event) {
    if (!navbar.contains(event.target) && !menuToggle.contains(event.target)) {
      navbar.classList.remove("active");
      menuToggle.classList.remove("active");
    }
  });

  const letters = document.querySelectorAll(".hero h1 span");
  letters.forEach((letter, index) => {
    letter.style.animationDelay = `${index * 0.1}s`;
  });
});
