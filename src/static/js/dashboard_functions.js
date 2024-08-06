function getAccounts() {
    // Запрос на получение счетов пользователя
    fetch('get-accounts', {
        method: 'GET'
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {

            // Добавление данных в переменную
            accounts = data.data

            // Удаление иконки загрузки
            const loading = document.getElementById('spinner-accounts')
            loading.style.display = 'none'

            updateAccounts(accounts)

            return accounts
        }
        if (data.status === 'error') {}
    })
    .catch((error) => {});
}


function getCategories() {
    // Запрос на получение категорий пользователя
    fetch('get-categories', {
        method: 'GET'
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {

            // Добавление данных в переменную
            categories = data.data

            // Удаление иконок загрузок
            const loading_exp = document.getElementById('spinner-expenses')
            const loading_inc = document.getElementById('spinner-incomes')
            loading_exp.style.display = 'none'
            loading_inc.style.display = 'none'

            // Блоки с категориями
            expensesBlock = document.getElementById('expenses-categories')
            incomesBlock = document.getElementById('incomes-categories')

            // Добавление категорий в HTML
            for (const category of categories) {

                const categoryHTML = categoryHTMLTemplate(category)

                if (category.category_type == 'expense') {
                    expensesBlock.insertAdjacentHTML('beforeend', categoryHTML);
                }
                if (category.category_type == 'income') {
                    incomesBlock.insertAdjacentHTML('beforeend', categoryHTML);
                }
            }

            updateCategories(categories)

            return categories
        }
        if (data.status === 'error') {}
    })
    .catch((error) => {});
}


function getOperations(params) {
    // Запрос на получение операций пользователя
    fetch('get-operations', {
        method: 'GET'
    })
    
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            operations = data.data
            return operations
        }
        if (data.status === 'error') {}
    })
    .catch((error) => {});
}


function createCategoryDict(categories, operations) {
    // Создание словаря {id категории: итог по операциям}
    let categoryDict = {}
    for (const category of categories) {
        categoryDict[category.category_id] = 0
    }
    
    // Добавление доходов и расходов по категориям
    for (const operation of operations) {
        let categoryID

        if (operation.operation_type == 'expense') {
            categoryID = operation.to_account
        } 
        if (operation.operation_type == 'income') {
            categoryID = operation.from_account
        }

        categoryDict[categoryID] = categoryDict[categoryID] + operation.amount
    }
    return categoryDict
}


function updateCategoryTotals(categoryDict) {
    // Получение блоков с категориями
    let categoriesAmountBlocks = document.getElementsByClassName('category-amount')
    categoriesAmountBlocks = Array.from(categoriesAmountBlocks)

    categoriesAmountBlocks.forEach(element => {
        // Получение данных из класса
        let categoryID = element.className.split(' ')[1]
        
        // Добавление итога по операциям
        element.textContent = `${categoryDict[categoryID]}`
    });
}


function updateTotals(operations) {
    const loading_operations = document.getElementById('spinner-operations')
    const placeholder_inc = document.getElementById('placeholder-incomes')
    const placeholder_exp = document.getElementById('placeholder-expenses')

    loading_operations.style.display = 'none'

    let total_incomes = 0
    let total_expenses = 0

    if (operations.length == 0) {
        placeholder_inc.textContent = 0
        placeholder_exp.textContent = 0
        return
    }

    // Определение валюты по первой операции
    let currency = operations[0].currency

    // Подсчет доходов/расходов
    for (const operation of operations) {
        if (operation.operation_type == 'expense') {
            total_expenses += operation.amount
        } 
        if (operation.operation_type == 'income') {
            total_incomes += operation.amount
        }
    }

    placeholder_inc.textContent = `${total_incomes} ${currency}`
    placeholder_exp.textContent = `${total_expenses} ${currency}`
}


function closeModal(modalID) {
    // Закрытие модального окна
    let modal = bootstrap.Modal.getInstance(document.getElementById(modalID))
    modal.hide();
}


function createAccount(jsonData) {
    // Создание счета
    return fetch('/create-account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch((error) => {});
}


function editAccount(jsonData) {
    // Редактирование счета
    return fetch('/edit-account', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch((error) => {});
}


function deleteAccount(jsonData) {
    // Удаление счета
    return fetch('/delete-account', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data            
    })
    .catch((error) => {});
}


function addLocalAccounts(account) {
    accounts.push(
        {
            account_id: account.account_id,
            title: account.title,
            balance: account.balance,
            currency: account.currency
        }
    )
}


function deleteLocalAccounts(accountID) {
    for (let i = 0; i < accounts.length; i++) {
        let account = accounts[i];

        if (accountID == account.account_id) {
            accounts.splice(i, 1);
            break;
        }
    }
}


function editLocalAccounts(new_account) {
    for (let i = 0; i < accounts.length; i++) {
        let account = accounts[i];

        if (new_account.id == account.account_id) {
            account.title = new_account.title;
            account.balance = new_account.balance;
            account.currency = new_account.currency;
            break;
        }
    }
}


function updateAccounts(accounts) {
    accountBlock = document.getElementById('accounts')

    // Добавление кнопки для создания счета
    accountBlock.innerHTML = '<button type="button" class="list-group-item list-group-item-action" data-bs-toggle="modal" data-bs-target="#create-account-modal"><i class="bi bi-plus-lg me-2"></i>Добавить счёт</button>'

    // Добавление счетов в HTML
    for (const account of accounts) {
        accountHTML = accountHTMLTemplate(account)
        accountBlock.insertAdjacentHTML('afterbegin', accountHTML);
    }

    // Добавление кнопок на счета для их изменения
    const accountEditElements = document.getElementsByClassName('account')
    for (let i = 0; i < accountEditElements.length; i++) {

        // Добавление нажатия для редактирования счетов
        accountEditElements[i].addEventListener('click', function(event) {

            let accountID = accountEditElements[i].className.split(' ')[1]

            // Очистка ошибки, при наличии
            const errorEditAccount = document.getElementById('alert-edit-account')
            errorEditAccount.style.display = 'none'
            errorEditAccount.textContent = ''

            for (let i = 0; i < accounts.length; i++) {

                let account = accounts[i]

                if (accountID == account.account_id) {
                    accountTitle = account.title
                    accountBalance = account.balance
                    accountCurrency = account.currency
                }
            }

            // Вставка данных в инпуты
            document.getElementById('account-edit-title').value = accountTitle
            document.getElementById('account-edit-balance').value = accountBalance
            document.getElementById('account-edit-currency').value = accountCurrency
            document.getElementById('account-edit-button').className = `${accountID} ${document.getElementById('account-edit-button').className}`
            document.getElementById('pre-delete-account-button').className = `${accountID} ${document.getElementById('pre-delete-account-button').className}`

        });
    }
}


function accountHTMLTemplate(account) {
    const accountHTML = `
        <button type="button" class="account ${account.account_id} list-group-item list-group-item-action" data-bs-toggle="modal" data-bs-target="#edit-account-modal" id="account-${account.account_id}">
            <h5 class="card-title" id="account-title-${account.account_id}">${account.title}</h5>
            <p class="card-text" id="account-balance-${account.account_id}">Баланс: ${account.balance} ${account.currency}</p>
        </button>
    `
    return accountHTML
}


function categoryHTMLTemplate(category) {
    const categoryHTML = `
        <div class="list-group w-100 mb-2 shadow-lg">
            <button type="button" class="category ${category.category_type} ${category.category_id} list-group-item list-group-item-action" style="border-left: 5px solid ${category.color}; border-top: None; border-right: None; border-bottom: None" data-bs-toggle="modal" data-bs-target="#create-operation-${category.category_type}-modal">
                <div class="d-flex">
                    <h5>${category.title}</h5>
                    <i class="bi bi-plus-lg me-2 ms-auto"></i>
                </div>
                <p class="${category.category_type} ${category.category_id} category-amount mb-1 placeholder-glow"><span class="placeholder col-6"></span></p>
            </button>
        </div>
    
    `
    return categoryHTML
}


function createCategory(jsonData) {
    // Создание категории
    return fetch('/create-category', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch((error) => {});
}


function addLocalCategories(category) {
    categories.push(
        {
            category_id: category.category_id,
            title: category.title,
            category_type: category.category_type,
            color: category.color
        }
    )
}


function updateCategories(categories) {
    // Добавление счетов в HTML
    expensesBlock = document.getElementById('expenses-categories')
    incomesBlock = document.getElementById('incomes-categories')
    expensesBlock.innerHTML = ''
    incomesBlock.innerHTML = ''

    for (const category of categories) {
        categoryHTML = categoryHTMLTemplate(category)
        if (category.category_type == 'expense') {
            expensesBlock.insertAdjacentHTML('beforeend', categoryHTML);
        }
        if (category.category_type == 'income') {
            incomesBlock.insertAdjacentHTML('beforeend', categoryHTML);
        }
    }

    // Добавление кнопок на категории для создания операций
    const categoryAddOperations = document.getElementsByClassName('category')
    for (let i = 0; i < categoryAddOperations.length; i++) {

        // Добавление нажатия для создания операции в категорий
        categoryAddOperations[i].addEventListener('click', function(event) {

            let categoryID = categoryAddOperations[i].className.split(' ')[2]

            for (let i = 0; i < categories.length; i++) {

                let category = categories[i]

                if (categoryID == category.category_id) {
                    categoryTitle = category.title
                    categoryType = category.category_type
                    categoryColor = category.color
                }
            }

            if (categoryType == 'expense') {
                // Очистка ошибки, при наличии
                const errorCreateExpense = document.getElementById('alert-create-operation-expense')
                errorCreateExpense.style.display = 'none'
                errorCreateExpense.textContent = ''

                // Вставка данных в инпуты
                document.getElementById('operation-expense-create-account-to').value = categoryID

                // Добавление id в класс кнопки изменения и удаления категории
                document.getElementById('category-expense-edit-button').className = `${categoryID} ${document.getElementById('category-expense-edit-button').className}`
                document.getElementById('category-edit-button').className = `${categoryID} ${document.getElementById('category-edit-button').className}`
                document.getElementById('pre-delete-category-button').className = `${categoryID} ${document.getElementById('pre-delete-category-button').className}`
            }
            if (categoryType == 'income') {
                // Очистка ошибки, при наличии
                const errorCreateIncome = document.getElementById('alert-create-operation-income')
                errorCreateIncome.style.display = 'none'
                errorCreateIncome.textContent = ''

                // Вставка данных в инпуты
                document.getElementById('operation-income-create-category').value = categoryID

                // Добавление id в класс кнопки изменения и удаления категории
                document.getElementById('category-income-edit-button').className = `${categoryID} ${document.getElementById('category-income-edit-button').className}`
                document.getElementById('category-edit-button').className = `${categoryID} ${document.getElementById('category-edit-button').className}`
                document.getElementById('pre-delete-category-button').className = `${categoryID} ${document.getElementById('pre-delete-category-button').className}`
            }
        });
    }

    // Вставка данных в инпут для изменения категории
    const buttonOpenEditExpenseCategory = document.getElementById('category-expense-edit-button')
    const buttonOpenEditIncomeCategory = document.getElementById('category-income-edit-button')
    const errorEditCategory = document.getElementById('alert-edit-category')
    let editCategoryTitle = document.getElementById('category-edit-title')
    let editCategoryColor = document.getElementById('category-edit-color')

    buttonOpenEditExpenseCategory.addEventListener('click', function(event) {
        errorEditCategory.style.display = 'none'
        categoryID = buttonOpenEditExpenseCategory.className.split(' ')[0]
        for (const category of categories) {
            if (category.category_id == categoryID) {
                editCategoryTitle.value = category.title
                editCategoryColor.value = category.color
            }
        }
    })
    buttonOpenEditIncomeCategory.addEventListener('click', function(event) {
        errorEditCategory.style.display = 'none'
        categoryID = buttonOpenEditIncomeCategory.className.split(' ')[0]
        for (const category of categories) {
            if (category.category_id == categoryID) {
                editCategoryTitle.value = category.title
                editCategoryColor.value = category.color
            }
        }
    })

    // Создание выбора категорий при создании операций
    document.getElementById('operation-expense-create-account-to').innerHTML = ''
    document.getElementById('operation-income-create-category').innerHTML = ''
    categories.forEach(category => {
        if (category.category_type == 'expense') {
            const option = document.createElement('option');
            option.value = category.category_id;
            option.textContent = category.title;

            // Добавляем option в select элемент
            document.getElementById('operation-expense-create-account-to').appendChild(option);
        }
        if (category.category_type == 'income') {
            const option = document.createElement('option');
            option.value = category.category_id;
            option.textContent = category.title;

            // Добавляем option в select элемент
            document.getElementById('operation-income-create-category').appendChild(option);
        }
    });
}


function editCategory(jsonData) {
    // Редактирование категории
    return fetch('/edit-category', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch((error) => {});
}


function editLocalCategories(new_category) {
    for (let i = 0; i < categories.length; i++) {
        let category = categories[i];

        if (new_category.id == category.category_id) {
            category.title = new_category.title;
            category.color = new_category.color;
            break;
        }
    }
}


function deleteLocalCategories(categoryID) {
    for (let i = 0; i < categories.length; i++) {
        let category = categories[i];

        if (categoryID == category.category_id) {
            categories.splice(i, 1);
            break;
        }
    }
}


function deleteCategory(jsonData) {
    // Удаление счета
    return fetch('/delete-category', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data            
    })
    .catch((error) => {});
}


function createOperation(jsonData) {
    // Создание категории
    return fetch('/create-operation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })

    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch((error) => {});
}


function addLocalOperation(operation) {
    operations.push(
        {
            operation_id: operation.operation_id,
            created_at: operation.created_at,
            operation_type: operation.operation_type,
            from_account: operation.from_account,
            to_account: operation.to_account,
            amount: operation.amount,
            currency: operation.currency,
            about: operation.about
        }
    )
}


function updateLocalAccount(accounts, operationInfo) {
    const amount = parseFloat(operationInfo.amount);

    for (let i = 0; i < accounts.length; i++) {
        let account = accounts[i];

        if (operationInfo.operation_type == 'expense' && operationInfo.from_account == account.account_id) {
            account.balance = account.balance - amount;
            break;
        } 
        if (operationInfo.operation_type == 'income' && operationInfo.to_account == account.account_id) {
            account.balance = account.balance + amount;
            break;
        }
    }
}


function deleteOperationWithID(operations, id) {
    for (let i = operations.length - 1; i >= 0; i--) {
        let operation = operations[i];

        if (id == operation.from_account || id == operation.to_account) {
            operations.splice(i, 1);
        }
    }
}


function updateAccountsSelectors(accounts) {
    // Получение элементов select
    const expenseSelect = document.getElementById('operation-create-expense-accounts');
    const incomeSelect = document.getElementById('operation-create-income-accounts');

    // Очистка содержимого select элементов
    expenseSelect.innerHTML = '';
    incomeSelect.innerHTML = '';

    // Создание выбора счета при создании операций
    accounts.forEach(account => {
        let option = document.createElement('option');
        option.value = account.account_id;
        option.textContent = account.title;

        // Добавляем option в select элемент
        document.getElementById('operation-create-expense-accounts').appendChild(option);

        option = document.createElement('option');
        option.value = `${account.account_id} `;
        option.textContent = account.title;
        document.getElementById('operation-create-income-accounts').appendChild(option);
    });
}


function updateCategorySelectors(categories) {
    // Создание выбора категорий при создании операций
    const expenseSelect = document.getElementById('operation-expense-create-account-to')
    const incomeSelect = document.getElementById('operation-income-create-category')

    // Очистка содержимого select элементов
    expenseSelect.innerHTML = '';
    incomeSelect.innerHTML = '';

    categories.forEach(category => {
        if (category.category_type == 'expense') {
            const option = document.createElement('option');
            option.value = category.category_id;
            option.textContent = category.title;

            // Добавляем option в select элемент
            document.getElementById('operation-expense-create-account-to').appendChild(option);
        }
        if (category.category_type == 'income') {
            const option = document.createElement('option');
            option.value = category.category_id;
            option.textContent = category.title;

            // Добавляем option в select элемент
            document.getElementById('operation-income-create-category').appendChild(option);
        }
    });
}