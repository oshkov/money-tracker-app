const form = document.getElementById('register-form')
const error_block = document.getElementById('alert')
const loading = document.getElementById('spinner')
const buttonText = document.getElementById('button-text')


form.addEventListener('submit', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы
    error_block.style.display = 'none' // Очистка ошибки, при наличии
    loading.style.display = 'block' // Вывод загрузки
    buttonText.style.display = 'none' // Очистка текста кнопки

    const data = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    const jsonData = JSON.stringify(data);

    // Отправляем данные на сервер
    fetch(`http://${ip}:8002/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        // console.log('Success:', data);
        loading.style.display = 'none'
        buttonText.style.display = 'block'
        if (data.status === 'success') {
            // Сохранение токена в Local Storage
            localStorage.setItem('access_token', data.data.access_token);

            error_block.style.display = 'none'
            window.location.href = '/dashboard';
        }
        if (data.status === 'error') {
            error_block.style.display = 'block'
            error_block.textContent = 'Пользователь с такой почтой уже зарегистрирован'
        }
    })
    .catch((error) => {
        error_block.style.display = 'block'
        error_block.textContent = 'Ошибка сервера'
        loading.style.display = 'none'
        buttonText.style.display = 'block'
    });
});