const theme_switcher_button = document.getElementById('theme-switcher-button')

theme_switcher_button.addEventListener('click', function(event) {
    fetch('/switch-theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Смена темы
        let newTheme = data.data
        document.documentElement.setAttribute('data-bs-theme', newTheme);

        // Смена иконки для кнопки
        let buttonIcon = document.getElementById('theme-icon')
        if (newTheme === 'light') {
            buttonIcon.className = 'bi bi-moon-fill';
        } else if (newTheme === 'dark') {
            buttonIcon.className = 'bi bi-sun-fill';
        }
    })
})