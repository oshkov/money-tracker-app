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
        document.getElementById('username').value = data.data.username
        document.getElementById('email').value = data.data.email

        if (data.status === 'error') {
            localStorage.removeItem('access_token')
            window.location.href = '/login'
        }
    })
} else {
    window.location.href = '/login'
}


const editProfileButton = document.getElementById('button-edit-profile')

editProfileButton.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

     // Очистка ошибки, при наличии
    const error = document.getElementById('alert')
    error.style.display = 'none'

    const data = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    const jsonData = JSON.stringify(data);

    console.log(jsonData)
    // Запрос на изменение профиля
    fetch(`http://${ip}:8002/edit-profile`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Перезагружаем страницу
            window.location.reload();
        }
        if (data.status === 'error') {
            if (data.detail === 'User with this email already registered') {
                error.style.display = 'block'
                error.textContent = 'Пользователь с такой почтой уже зарегистрирован'
            } else if (data.detail === 'Password is incorrect') {
                error.style.display = 'block'
                error.textContent = 'Пароль неверный'
            } else {
                error.style.display = 'block'
                error.textContent = 'Ошибка сервера'
            }
        }
    })
    .catch((error) => {
        console.log(error)
    });
})