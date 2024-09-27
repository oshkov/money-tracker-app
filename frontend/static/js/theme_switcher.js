const theme_switcher_button = document.getElementById('theme-switcher-button')

// Функиция добавления данных в куки
function setCookie(name, value, days) {
    let expires = ""
    if (days) {
        const date = new Date()
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000))
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/"
}

// Функиция получения данных из куки
function getCookie(name) {
    let nameEQ = name + "="
    let cookiesArray = document.cookie.split(';')
    for (let i = 0; i < cookiesArray.length; i++) {
        let cookie = cookiesArray[i].trim()     // Убираем лишние пробелы
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length, cookie.length)
        }
    }
    return null     // Если cookie с таким именем не найдено
}


// Создание куки для темы если ее нет
let theme = getCookie('theme')
if (theme === null) {
    setCookie("theme", null, 1)
}


theme_switcher_button.addEventListener('click', function(event) {
    // Получение темы из куки
    let theme = getCookie('theme')

    let newTheme
    let buttonIcon = document.getElementById('theme-icon')

    if (theme === 'light' || theme === '') {
        newTheme = 'dark'
        buttonIcon.className = 'bi bi-moon-fill'        // Смена иконки для кнопки

    } else if (theme === 'dark') {
        newTheme = 'light'
        buttonIcon.className = 'bi bi-sun-fill'     // Смена иконки для кнопки
    }
    document.documentElement.setAttribute('data-bs-theme', newTheme)

    // Установка темы в куки
    setCookie("theme", newTheme, 1)
})