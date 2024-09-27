function postHTMLTemplate(post) {
    const postHTML = `
        <div class="col-md-6 mt-4">
            <div class="h-100 p-5 bg-body-tertiary border rounded-3" id="news-${post.news_id}">
                <h2>${post.title}</h2>
                <p>${post.text}</p>
                <button class="btn btn-primary" type="button" disabled>Читать</button>
            </div>
        </div>
    `
    return postHTML
}


function updateNews(news) {
    newsBlock = document.getElementById('news')
    
    if (news === null) {
        newsBlock.innerHTML = '<p>Новостей нет</p>'
        return
    }

    newsBlock.innerHTML = ''

    // Добавление счетов в HTML
    for (const post of news) {
        postHTML = postHTMLTemplate(post)
        newsBlock.insertAdjacentHTML('afterbegin', postHTML);
    }
}
