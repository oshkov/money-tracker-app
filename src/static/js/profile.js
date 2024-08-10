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

    // Запрос на изменение профиля
    fetch('/edit-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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
    .catch((error) => {});
})