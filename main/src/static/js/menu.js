const logout = document.getElementById('logout')

logout.addEventListener('click', function(event) {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: null
    })
})