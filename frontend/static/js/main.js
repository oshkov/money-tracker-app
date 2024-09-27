// Запрос на получение новостей
fetch(`http://${ip}:8001/get-news`, {
    method: 'GET'
})

.then(response => response.json())
.then(data => {
    updateNews(data.data)
})
.catch((error) => {
    updateNews(null)
});