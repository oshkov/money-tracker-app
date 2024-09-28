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
        if (data.status === 'error') {
            localStorage.removeItem('access_token')
            window.location.href = '/login'
        }
    })
} else {
    window.location.href = '/login'
}


let accounts = null // Переменная счетов пользователя
let categories = null // Переменная категорий пользователя
let operations = null // Переменная операций пользователя


// Получение данных
getAccounts().then(data => {
    accounts = data.data
})

getCategories().then(data => {
    categories = data.data
})

getOperations().then(data => {
    operations = data.data
})


// Проверка на получение данных при запуске страницы
let intervalID = setInterval(() => {
    if (categories != null && operations != null && accounts != null) {
        clearInterval(intervalID)

        updateOperationsList(operations, categories, accounts)
    }
}, 20);


/*

Удаление операции

*/
const preDeleteOperationButton = document.getElementById('pre-delete-operation-button')
const deleteOperationButton = document.getElementById('delete-operation-button')

preDeleteOperationButton.addEventListener('click', function() {
    let operationID = preDeleteOperationButton.className.split(' ')[0]
    deleteOperationButton.className = `${operationID} ${deleteOperationButton.className}`
})

deleteOperationButton.addEventListener('click', function() {
    const operationID = deleteOperationButton.className.split(' ')[0]

    const data = {
        id: operationID
    };
    const jsonData = JSON.stringify(data);

    deleteOperation(jsonData).then(data => {
        if (data.status == 'success') {
            // Операция удаляется из переменной
            deleteLocalOperations(operationID)

            // Обновление списка операций
            updateOperationsList(operations, categories, accounts)

            closeModal('delete-operation-modal')
        }
    });
})


/*

Редактирование операции

*/
const errorEditOperation = document.getElementById('alert-edit-operation')
errorEditOperation.style.display = 'none'
const buttonEditOperation = document.getElementById('operation-edit-button')

buttonEditOperation.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    // Очистка ошибки, при наличии
    errorEditOperation.style.display = 'none'
    errorEditOperation.textContent = ''

    // Получение данных из формы
    const operationID = document.getElementById('operation-edit-button').className.split(' ')[0]
    const operationType = document.getElementById('operation-edit-button').className.split(' ')[1]
    const fromAccount = document.getElementById('operation-edit-from-account').value
    const toAccount = document.getElementById('operation-edit-to-account').value
    const amount = document.getElementById('operation-edit-amount').value
    const currency = document.getElementById('operation-edit-currency').value
    let about = document.getElementById('operation-edit-about').value
    about = about === '' ? null : about;

    if (fromAccount === '' || toAccount === '' || amount === '' || currency === '' || about === '') {
        errorEditOperation.style.display = 'block'
        errorEditOperation.textContent = 'Введите все данные' // Очистка ошибки, при наличии
        return
    }

    let operationBeforeEdit
    for (let i = 0; i < operations.length; i++) {
        let operation = operations[i];

        if (operationID == operation.operation_id) {
            operationBeforeEdit = operation
            break;
        }
    }

    const newOperation = {
        id: operationID,
        from_account: fromAccount,
        to_account: toAccount,
        amount: amount,
        currency: currency,
        about: about
    };
    const jsonData = JSON.stringify(newOperation);

    editOperation(jsonData).then(edit => {
        if (edit.status == 'success') {
            // Счет удаляется из переменной
            editLocalOperations(newOperation)

            // Обновление списка операций
            updateOperationsList(operations, categories, accounts)

            closeModal('edit-operation-modal')
        }
        if (edit.status == 'error') {
            errorEditOperation.style.display = 'block'
            errorEditOperation.textContent = 'Произошла ошибка'
        }
    });
});