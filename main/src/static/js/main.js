getNews().then(data => {
    if (data.status == 'success') {
        updateNews(data.data)
    }
    if (data.status == 'error') {
        updateNews(null)
    }
});