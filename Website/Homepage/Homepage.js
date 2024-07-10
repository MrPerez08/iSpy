document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('changeTextButton');
    const heroContent = document.querySelector('.hero-content p');

    button.addEventListener('click', () => {
        heroContent.textContent = 'You clicked the button! The text has changed.';
    });
});
