const logout = document.getElementById('logout-button')

logout.addEventListener('click', function(event) {
    localStorage.removeItem('access_token')
})


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
            document.getElementById('username-menu').textContent = data.data.username
        }
    })
} else {
    window.location.href = '/login'
}