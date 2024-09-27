// Получаем токен из localStorage
const token = localStorage.getItem('access_token')

// Если токен существует, происходит запрос на получение данных пользователя
if (token) {
    fetch(`http://${ip}:8002/get-current-user`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.href = '/dashboard'
        } else {
            localStorage.removeItem('access_token')
        }
    })
}


const form = document.getElementById('login-form')
const error_block = document.getElementById('alert')
const loading = document.getElementById('spinner')
const buttonText = document.getElementById('button-text')


form.addEventListener('submit', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы
    error_block.style.display = 'none' // Очистка ошибки, при наличии
    loading.style.display = 'block' // Вывод загрузки
    buttonText.style.display = 'none' // Очистка текста кнопки

    const data = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    const jsonData = JSON.stringify(data);

    // Отправляем данные на сервер
    fetch(`http://${ip}:8002/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData,
        credentials: "include",
    })

    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        loading.style.display = 'none'
        buttonText.style.display = 'block'

        if (data.status === 'success') {
            error_block.style.display = 'none'
            // Сохранение токена в Local Storage
            localStorage.setItem('access_token', data.data.access_token);

            window.location.href = '/dashboard'
        }
        if (data.status === 'error') {
            error_block.style.display = 'block'
            error_block.textContent = 'Неверный email или пароль. Пожалуйста, проверьте введенные данные и попробуйте снова.'
        }
        
    })
    .catch((error) => {
        error_block.style.display = 'block'
        error_block.textContent = 'Ошибка сервера'
        loading.style.display = 'none'
        buttonText.style.display = 'block'
    });
});