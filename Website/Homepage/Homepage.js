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
});

document.addEventListener("DOMContentLoaded", function () {
  const predatorButton = document.querySelector(".opt1");
  const serverButton = document.querySelector(".opt2");
  const questionText = document.querySelector(".hero-content h1");
  const buttons = document.querySelectorAll(".hero-content button");

  predatorButton.addEventListener("click", function () {
    document.querySelectorAll(".pedo").forEach(function (element) {
      element.style.display = "block";
    });
    document.querySelectorAll(".server").forEach(function (element) {
      element.style.display = "none";
    });
    hideQuestionAndButtons();
  });

  serverButton.addEventListener("click", function () {
    document.querySelectorAll(".server").forEach(function (element) {
      element.style.display = "block";
    });
    document.querySelectorAll(".pedo").forEach(function (element) {
      element.style.display = "none";
    });
    hideQuestionAndButtons();
  });

  function hideQuestionAndButtons() {
    questionText.style.display = "none";
    buttons.forEach(function (button) {
      button.style.display = "none";
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const predatorButton = document.querySelector(".opt1");
  const serverButton = document.querySelector(".opt2");
  const questionText = document.querySelector(".hero-content h1");
  const buttons = document.querySelectorAll(".hero-content button");
  const buttonContainer = document.querySelector(".button-container"); // Selecting the button container

  predatorButton.addEventListener("click", function () {
    document.querySelectorAll(".pedo").forEach(function (element) {
      element.style.display = "block";
    });
    document.querySelectorAll(".server").forEach(function (element) {
      element.style.display = "none";
    });
    hideQuestionAndButtons();
  });

  serverButton.addEventListener("click", function () {
    document.querySelectorAll(".server").forEach(function (element) {
      element.style.display = "block";
    });
    document.querySelectorAll(".pedo").forEach(function (element) {
      element.style.display = "none";
    });
    hideQuestionAndButtons();
  });

  function hideQuestionAndButtons() {
    questionText.style.display = "none";
    buttons.forEach(function (button) {
      button.style.display = "none";
    });
    buttonContainer.style.display = "none"; // Hide the entire button container
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const opt1Button = document.querySelector(".opt1");
  const opt2Button = document.querySelector(".opt2");

  function showNextButton() {
    const nextButtons = document.querySelectorAll(".next-button");
    nextButtons.forEach((button) => {
      button.style.display = "flex";
      button.style.margin = "0 auto"; // Center the button horizontally
    });
  }

  opt1Button.addEventListener("click", showNextButton);
  opt2Button.addEventListener("click", showNextButton);
});

// JavaScript for toggling X button visibility
function toggleXButton() {
  var xButtonContainer = document.getElementById("xButtonContainer");
  xButtonContainer.style.display = "block";
}
const xButton = document.querySelector(".close-button");
xButton.addEventListener("click", function () {
  xButtonContainer.style.display = "none";
  document.querySelectorAll(".pedo").forEach(function (element) {
    element.style.display = "none";
  });
  document.querySelectorAll(".server").forEach(function (element) {
    element.style.display = "none";
  });
  document.querySelector(".button-container").style.display = "flex";
  document.querySelector(".opt1").style.display = "flex";
  //document.querySelector(".opt2").style.display = "flex";
  document.querySelector("h1.main").style.display = "block";
  document.querySelector(".hero h1 span").style.display = "inline-block";
});
