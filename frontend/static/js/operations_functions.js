function getAccounts() {
    // Запрос на получение счетов пользователя
    return fetch(`http://${ip}:8003/get-accounts`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            return data
        }
        if (data.status === 'error') {}
    })
    .catch((error) => {});
}


function getCategories() {
    // Запрос на получение категорий пользователя
    return fetch(`http://${ip}:8003/get-categories`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            return data
        }
        if (data.status === 'error') {}
    })
    .catch((error) => {});
}


function getOperations() {
    // Запрос на получение операций пользователя
    return fetch(`http://${ip}:8003/get-operations`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            return data
        }
        if (data.status === 'error') {}
    })
    .catch((error) => {});
}


function operationHTMLTemplate(operation, categories, accounts) {
    let color
    let from_account = null
    let category_color = null
    let to_account = null
    let amount
    let about = operation.about
    about = about === null ? '' : about;

    if (operation.operation_type == 'expense') {
        color = 'red'
        from_account = null
        to_account = null
        for (const account of accounts) {
            if (account.account_id == operation.from_account) {
                from_account = account.title
            }
        }
        for (const category of categories) {
            if (category.category_id == operation.to_account) {
                to_account = category.title
                category_color = category.color
            }
        }
        amount = `-${operation.amount}`
    }
    if (operation.operation_type == 'income') {
        color = 'green'
        from_account = null
        to_account = null
        for (const category of categories) {
            if (category.category_id == operation.from_account) {
                from_account = category.title
                category_color = category.color
            }
        }
        for (const account of accounts) {
            if (account.account_id == operation.to_account) {
                to_account = account.title
            }
        }
        amount = `+${operation.amount}`
    }

    let operationHTML =  `
    <button type="button" class="${operation.operation_id} operation list-group-item list-group-item-action" style="border-left: 5px solid ${category_color};" data-bs-toggle="modal" data-bs-target="#edit-operation-modal">
        <div class="row me-auto">
            <div class="col-8">
                <div class="fs-5 fw-bold" style="color: ${color};">${amount} ${operation.currency}</div>
                <p class="fw-light mb-0">${operation.created_at}</p>
                <p class="fw-light mb-0">${from_account} <i class="bi bi-arrow-right-short"></i> ${to_account}</p>
                <p class="fs-5 mb-1">${about}</p>
            </div>
            <div class="col-4">
                <div class="fs-4 text-end"><i class="bi bi-pencil-square"></i></div>
            </div>
        </div>
    </button>
    `
    return operationHTML
}


function updateOperationsList(operations, categories, accounts) {
    // Обновление операций в HTML
    operationsBlock = document.getElementById('operations-list')
    operationsBlock.innerHTML = ''

    // Удаление иконки загрузки
    const loading = document.getElementById('spinner-operations')
    loading.style.display = 'none'

    for (const operation of operations) {

        operationHTML = operationHTMLTemplate(operation, categories, accounts)

        operationsBlock.insertAdjacentHTML('beforeend', operationHTML)

        // Найти последнюю добавленную кнопку и назначить ей обработчик событий
        const operationButtons = operationsBlock.querySelectorAll('.operation')
        const latestButton = operationButtons[operationButtons.length - 1]
        
        // Вставка данных в инпуты при открытии редактирования операции
        latestButton.addEventListener('click', function() {

            // Добавление id в кнопку удаления и изменения операции
            document.getElementById('pre-delete-operation-button').className = `${operation.operation_id} ${document.getElementById('pre-delete-operation-button').className}`
            document.getElementById('operation-edit-button').className = `${operation.operation_id} ${operation.operation_type} ${document.getElementById('operation-edit-button').className}`

            let errorEditOperation = document.getElementById('alert-edit-operation')
            errorEditOperation.style.display = 'none'
            errorEditOperation.textContent = null

            const operationID = latestButton.className.split(' ')[0]
            let operationType
            let fromAccount
            let toAccount
            let amount
            let about

            for (const operation of operations) {
                if (operationID == operation.operation_id) {
                    operationType = operation.operation_type
                    fromAccount = operation.from_account
                    toAccount = operation.to_account
                    amount = operation.amount
                    about = operation.about
                }
            }

            if (operationType == 'expense') {
                document.getElementById('operation-edit-amount-label').textContent = 'Расход'
                document.getElementById('operation-edit-from-account-label').textContent = 'Со счета'
                document.getElementById('operation-edit-to-account-label').textContent = 'На категорию'
                updateAccountsSelectors(accounts, 'operation-edit-from-account')
                updateCtegoriesSelectors(categories, 'operation-edit-to-account')
            }
            if (operationType == 'income') {
                document.getElementById('operation-edit-amount-label').textContent = 'Доход'
                document.getElementById('operation-edit-from-account-label').textContent = 'С категории'
                document.getElementById('operation-edit-to-account-label').textContent = 'На счет'
                updateAccountsSelectors(accounts, 'operation-edit-to-account')
                updateCtegoriesSelectors(categories, 'operation-edit-from-account')
            }

            document.getElementById('operation-edit-amount').value = amount
            document.getElementById('operation-edit-about').value = about
            document.getElementById('operation-edit-from-account').value = fromAccount
            document.getElementById('operation-edit-to-account').value = toAccount
        });
    }
}


function updateAccountsSelectors(accounts, blockID) {
    // Получение элементов select
    const accountSelect = document.getElementById(blockID)

    // Очистка содержимого select элементов
    accountSelect.innerHTML = '';

    // Создание выбора счета при изменении операций
    accounts.forEach(account => {
        let option = document.createElement('option');
        option.value = account.account_id;
        option.textContent = account.title;

        // Добавляем option в select элемент
        accountSelect.appendChild(option);
    });
}


function updateCtegoriesSelectors(categories, blockID) {
    // Получение элементов select
    const categoriesSelect = document.getElementById(blockID)

    // Очистка содержимого select элементов
    categoriesSelect.innerHTML = '';

    // Создание выбора категорий при изменении операции
    categories.forEach(category => {
        let option = document.createElement('option');
        option.value = category.category_id;
        option.textContent = category.title;

        // Добавляем option в select элемент
        categoriesSelect.appendChild(option);
    });
}


function deleteOperation(jsonData) {
    // Удаление операции
    return fetch(`http://${ip}:8003/delete-operation`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch((error) => {});
}


function deleteLocalOperations(operationID) {
    for (let i = 0; i < operations.length; i++) {
        let operation = operations[i];

        if (operationID == operation.operation_id) {
            operations.splice(i, 1);
            break;
        }
    }
}


function closeModal(modalID) {
    // Закрытие модального окна
    let modal = bootstrap.Modal.getInstance(document.getElementById(modalID))
    modal.hide();
}


function editLocalOperations(new_operation) {
    for (let i = 0; i < operations.length; i++) {
        let operation = operations[i];

        if (new_operation.id == operation.operation_id) {
            operation.from_account = new_operation.from_account,
            operation.to_account = new_operation.to_account,
            operation.amount = new_operation.amount,
            operation.currency = new_operation.currency,
            operation.about = new_operation.about
            break;
        }
    }
}


function editOperation(jsonData) {
    // Редактирование счета
    return fetch(`http://${ip}:8003/edit-operation`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch((error) => {});
}


function editAccountBalance(newOperation, operationBeforeEdit) {
    let data
    let accountInfo

    if (operationBeforeEdit.operation_type == 'income') {
        // Получение данных о счете
        for (const account of accounts) {
            if (operationBeforeEdit.to_account == account.account_id) {
                accountInfo = account
            }
        }

        newBalance = accountInfo.balance - operationBeforeEdit.amount + parseFloat(newOperation.amount)
        data = {
            id: accountInfo.account_id,
            title: accountInfo.title,
            balance: newBalance,
            currency: accountInfo.currency
        }
    }
    if (operationBeforeEdit.operation_type == 'expense') {
        // Получение данных о счете
        for (const account of accounts) {
            if (operationBeforeEdit.from_account == account.account_id) {
                accountInfo = account
            }
        }

        newBalance = accountInfo.balance + operationBeforeEdit.amount - parseFloat(newOperation.amount)
        data = {
            id: accountInfo.account_id,
            title: accountInfo.title,
            balance: newBalance,
            currency: accountInfo.currency
        }
    }
    const jsonData = JSON.stringify(data);

    // Редактирование счета
    fetch(`http://${ip}:8003/edit-account`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: jsonData
    })
}


function editAccountBalanceAfterDeleteOperation(operationID) {
    let operationInfo
    let accountInfo
    let newBalance

    // Получение данных об операции
    for (const operation of operations) {
        if (operationID == operation.operation_id) {
            operationInfo = operation
        }
    }

    if (operationInfo.operation_type == 'income') {
        for (const account of accounts) {
            if (operationInfo.to_account == account.account_id) {
                accountInfo = account
            }
        }
        newBalance = parseFloat(accountInfo.balance) - parseFloat(operationInfo.amount)
    }
    if (operationInfo.operation_type == 'expense') {
        for (const account of accounts) {
            if (operationInfo.from_account == account.account_id) {
                accountInfo = account
            }
        }
        newBalance = parseFloat(accountInfo.balance) + parseFloat(operationInfo.amount)
    }
    
    data = {
        id: accountInfo.account_id,
        title: accountInfo.title,
        balance: newBalance,
        currency: accountInfo.currency
    }

    editLocalAccounts(data)

    const jsonData = JSON.stringify(data);

    // Редактирование счета
    fetch(`http://${ip}:8003/edit-account`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(data)
        }
        if (data.status === 'error') {
            console.log(data)
        }
    })
    .catch((error) => {console.log(error)});
}


function editLocalAccounts(new_account) {
    for (let i = 0; i < accounts.length; i++) {
        let account = accounts[i];

        if (new_account.id == account.account_id) {
            account.balance = new_account.balance;
            break;
        }
    }
}