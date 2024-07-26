const form = document.getElementById('login-form')
const error = document.getElementById('alert')
const loading = document.getElementById('spinner')
const buttonText = document.getElementById('button-text')

error.style.display = 'none'
loading.style.display = 'none'


form.addEventListener('submit', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы
    error.style.display = 'none' // Очистка ошибки, при наличии
    loading.style.display = 'block' // Вывод загрузки
    buttonText.style.display = 'none' // Очистка текста кнопки

    const data = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    const jsonData = JSON.stringify(data);

    // Отправляем данные на сервер
    fetch(this.action, {
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
            error.style.display = 'none'
            window.location.href = '/dashboard'
        }
        if (data.status === 'error') {
            error.style.display = 'block'
            error.textContent = 'Неверный email или пароль. Пожалуйста, проверьте введенные данные и попробуйте снова.'
        }
        
    })
    .catch((error) => {
        // console.error('Error:', error);
    });
});