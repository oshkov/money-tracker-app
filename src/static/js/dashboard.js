let accounts = null // Переменная счетов пользователя
let categories = null // Переменная категорий пользователя
let operations = null // Переменная операций пользователя


// Получение данных
accounts = getAccounts()
categories = getCategories()
operations = getOperations()


// Проверка на получение данных при запуске страницы
let intervalID = setInterval(() => {
    if (categories != null && operations != null && accounts != null) {
        clearInterval(intervalID)

        // Добавление общего подсчета доходов и расходов
        updateTotals(operations)

        // Добавление доходов и расходов по категориям 
        categoryDict = createCategoryDict(categories, operations)
        updateCategoryTotals(categoryDict)

        // Создание выбора счета при создании операций
        updateAccountsSelectors(accounts)
    }
}, 20);


/*

Создание счета

*/
// Очистка ошибки, при наличии
const errorAccount = document.getElementById('alert-create-account')
errorAccount.style.display = 'none'
const buttonCreateAccount = document.getElementById('account-create-button')

buttonCreateAccount.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    // Очистка ошибки, при наличии
    errorAccount.style.display = 'none'
    errorAccount.textContent = ''

    // Получение данных из формы
    const accountTitle = document.getElementById('account-create-title').value
    const accountBalance = document.getElementById('account-create-balance').value
    const accountCurrency = document.getElementById('account-create-currency').value

    if (accountTitle === '' || accountBalance === '' || accountCurrency === '') {
        errorAccount.style.display = 'block'
        errorAccount.textContent = 'Введите все данные' // Очистка ошибки, при наличии
        return
    }

    const data = {
        title: accountTitle,
        balance: accountBalance,
        currency: accountCurrency
    };
    const jsonData = JSON.stringify(data);

    createAccount(jsonData).then(data => {
        if (data.status == 'success') {
            // Счет добавляется в переменную
            addLocalAccounts(data.data)

            // Обновление счетов
            updateAccounts(accounts)

            // Создание выбора счета при создании операций
            updateAccountsSelectors(accounts)

            errorAccount.style.display = 'none'
            closeModal('create-account-modal')

            document.getElementById('account-create-title').value = ''
            document.getElementById('account-create-balance').value = ''
            document.getElementById('account-create-currency').value = ''
        }
        if (data.status == 'error') {
            errorAccount.style.display = 'block'
            errorAccount.textContent = 'Такой счет уже создан'
        }
    });
});


/*

Редактирование счета

*/
const errorEditAccount = document.getElementById('alert-edit-account')
errorEditAccount.style.display = 'none'
const buttonEditAccount = document.getElementById('account-edit-button')

buttonEditAccount.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    // Очистка ошибки, при наличии
    errorEditAccount.style.display = 'none'
    errorEditAccount.textContent = ''

    // Получение данных из формы
    const accountID = document.getElementById('account-edit-button').className.split(' ')[0]
    const accountTitle = document.getElementById('account-edit-title').value
    const accountBalance = document.getElementById('account-edit-balance').value
    const accountCurrency = document.getElementById('account-edit-currency').value

    if (accountTitle === '' || accountBalance === '' || accountCurrency === '') {
        errorEditAccount.style.display = 'block'
        errorEditAccount.textContent = 'Введите все данные' // Очистка ошибки, при наличии
        return
    }

    const data = {
        id: accountID,
        title: accountTitle,
        balance: accountBalance,
        currency: accountCurrency
    };
    const jsonData = JSON.stringify(data);

    editAccount(jsonData).then(edit => {
        if (edit.status == 'success') {
            editLocalAccounts(data)

            // Обновление счетов
            updateAccounts(accounts)

            // Создание выбора счета при создании операций
            updateAccountsSelectors(accounts)

            errorEditAccount.style.display = 'none'
            closeModal('edit-account-modal')
        }
        if (edit.status == 'error') {
            errorEditAccount.style.display = 'block'
            errorEditAccount.textContent = 'Такой счет уже создан'
        }
    });
});


/*

Удаление счета

*/
const preDeleteAccountButton = document.getElementById('pre-delete-account-button')
const deleteAccountButton = document.getElementById('delete-account-button')

preDeleteAccountButton.addEventListener('click', function(event) {
    let accountID = preDeleteAccountButton.className.split(' ')[0]
    deleteAccountButton.className = `${accountID} ${document.getElementById('delete-account-button').className}`
})

deleteAccountButton.addEventListener('click', function(event) {
    const accountID = deleteAccountButton.className.split(' ')[0]

    const data = {
        id: accountID
    };
    const jsonData = JSON.stringify(data);

    deleteAccount(jsonData).then(edit => {
        if (edit.status == 'success') {
            // Счет удаляется из переменной
            deleteLocalAccounts(accountID)

            // Обновление счетов
            updateAccounts(accounts)

            // Удаление всех операций связанных с этим счетом
            deleteOperationWithID(operations, accountID)

            // Добавление общего подсчета доходов и расходов
            updateTotals(operations)

            // Создание выбора счета при создании операций
            updateAccountsSelectors(accounts)

            // Обновление доходов и расходов по категориям
            categoryDict = createCategoryDict(categories, operations)
            updateCategoryTotals(categoryDict)

            closeModal('delete-account-modal')
        }
    });
})


/*

Создание категории

*/
// Очистка ошибки, при наличии
const errorCreateCategory = document.getElementById('alert-create-category')
errorCreateCategory.style.display = 'none'
const buttonCreateCategory = document.getElementById('category-create-button')

buttonCreateCategory.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    // Очистка ошибки, при наличии
    errorCreateCategory.style.display = 'none'
    errorCreateCategory.textContent = ''

    // Получение данных из формы
    const categoryTitle = document.getElementById('category-create-title').value
    const categoryType = document.getElementById('category-create-type').value
    const categoryColor = document.getElementById('category-create-color').value

    if (categoryTitle === '' || categoryType === '' || categoryColor === '') {
        errorCreateCategory.style.display = 'block'
        errorCreateCategory.textContent = 'Введите все данные' // Очистка ошибки, при наличии
        return
    }

    const data = {
        title: categoryTitle,
        category_type: categoryType,
        color: categoryColor
    };
    const jsonData = JSON.stringify(data);

    createCategory(jsonData).then(data => {
        if (data.status == 'success') {
            // Категория добавляется в переменную
            addLocalCategories(data.data)

            // Обновление категорий
            updateCategories(categories)

            // Обновление доходов и расходов по категориям
            categoryDict = createCategoryDict(categories, operations)
            updateCategoryTotals(categoryDict)

            errorCreateCategory.style.display = 'none'
            closeModal('create-category-modal')

            document.getElementById('category-create-title').value = ''
            document.getElementById('category-create-type').value = ''
            document.getElementById('category-create-color').value = '#0008FF'
        }
        if (data.status == 'error') {
            errorCreateCategory.style.display = 'block'
            errorCreateCategory.textContent = 'Такая категория уже создана'
        }
    });
});


/*

Редактирование категории

*/
// Очистка ошибки, при наличии
const errorEditCategory = document.getElementById('alert-edit-category')
errorEditCategory.style.display = 'none'
const buttonEditCategory = document.getElementById('category-edit-button')

buttonEditCategory.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    // Очистка ошибки, при наличии
    errorEditCategory.style.display = 'none'
    errorEditCategory.textContent = ''

    // Получение данных из формы
    const categoryID = buttonEditCategory.className.split(' ')[0]
    const categoryTitle = document.getElementById('category-edit-title').value
    const categoryColor = document.getElementById('category-edit-color').value

    if (categoryTitle === '' || categoryType === '' || categoryColor === '') {
        errorEditCategory.style.display = 'block'
        errorEditCategory.textContent = 'Введите все данные' // Очистка ошибки, при наличии
        return
    }

    const data = {
        id: categoryID,
        title: categoryTitle,
        color: categoryColor
    };
    const jsonData = JSON.stringify(data);

    editCategory(jsonData).then(edit => {
        if (edit.status == 'success') {
            // Изменение категории в переменной
            editLocalCategories(data)

            // Обновление категорий
            updateCategories(categories)

            // Обновление доходов и расходов по категориям
            categoryDict = createCategoryDict(categories, operations)
            updateCategoryTotals(categoryDict)

            errorCreateCategory.style.display = 'none'
            closeModal('edit-category-modal')

        }
        if (edit.status == 'error') {
            errorEditCategory.style.display = 'block'
            errorEditCategory.textContent = 'Такая категория уже создана'
        }
    });
});


/*

Удаление категории

*/
const preDeleteCategoryButton = document.getElementById('pre-delete-category-button')
const deleteCategoryButton = document.getElementById('delete-category-button')

preDeleteCategoryButton.addEventListener('click', function(event) {
    let categoryID = preDeleteCategoryButton.className.split(' ')[0]
    deleteCategoryButton.className = `${categoryID} ${document.getElementById('delete-category-button').className}`
})

deleteCategoryButton.addEventListener('click', function(event) {
    const categoryID = deleteCategoryButton.className.split(' ')[0]

    const data = {
        id: categoryID
    };
    const jsonData = JSON.stringify(data);

    deleteCategory(jsonData).then(data => {
        if (data.status == 'success') {
            // Счет удаляется из переменной
            deleteLocalCategories(categoryID)

            // Обновление счетов
            updateCategories(categories)

            // Обновление доходов и расходов по категориям
            categoryDict = createCategoryDict(categories, operations)
            updateCategoryTotals(categoryDict)

            // Удаление всех операций связанных с этой категорией
            deleteOperationWithID(operations, categoryID)

            // Добавление общего подсчета доходов и расходов
            updateTotals(operations)

            // Создание выбора категорий при создании операций
            updateCategorySelectors(categories)

            closeModal('delete-category-modal')
        }
    });
})


/*

Создание расхода

*/
// Очистка ошибки, при наличии
const errorCreateExpense = document.getElementById('alert-create-operation-expense')
errorCreateExpense.style.display = 'none'
const buttonCreateExpense = document.getElementById('operation-create-expense-button')

buttonCreateExpense.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    // Очистка ошибки, при наличии
    errorCreateExpense.style.display = 'none'
    errorCreateExpense.textContent = ''

    // Получение данных из формы
    const operationType = 'expense'
    const accountFrom = document.getElementById('operation-create-expense-accounts').value
    const accountTo = document.getElementById('operation-expense-create-account-to').value
    const amount = document.getElementById('operation-create-expense-amount').value
    const currency = document.getElementById('operation-create-expense-currency').value
    let about = document.getElementById('operation-create-expense-about').value
    about = about === "" ? null : about;

    if (accountFrom === '' || accountTo === '' || amount === '') {
        errorCreateExpense.style.display = 'block'
        errorCreateExpense.textContent = 'Введите все данные' // Очистка ошибки, при наличии
        return
    }

    const operationInfo = {
        operation_type: operationType,
        from_account: accountFrom,
        to_account: accountTo,
        amount: amount,
        currency: currency,
        about: about
    };
    const jsonData = JSON.stringify(operationInfo);

    createOperation(jsonData).then(data => {
        if (data.status == 'success') {
            // Операция добавляется в переменную
            addLocalOperation(data.data)

            // Обновление общих раходов и доходов
            updateTotals(operations)

            // Обновление доходов и расходов по категориям
            categoryDict = createCategoryDict(categories, operations)
            updateCategoryTotals(categoryDict)

            // Обновление счета с которого была сделана операция
            updateLocalAccount(accounts, operationInfo)

            // Обновление счетов
            updateAccounts(accounts)

            errorCreateExpense.style.display = 'none'
            closeModal('create-operation-expense-modal')
        }
    });
});


/*

Создание дохода

*/
// Очистка ошибки, при наличии
const errorCreateIncome = document.getElementById('alert-create-operation-income')
errorCreateIncome.style.display = 'none'
const buttonCreateIncome = document.getElementById('operation-create-income-button')

buttonCreateIncome.addEventListener('click', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    // Очистка ошибки, при наличии
    errorCreateIncome.style.display = 'none'
    errorCreateIncome.textContent = ''

    // Получение данных из формы
    const operationType = 'income'
    const accountFrom = document.getElementById('operation-income-create-category').value
    const accountTo = document.getElementById('operation-create-income-accounts').value.trim()
    const amount = document.getElementById('operation-create-income-amount').value
    const currency = document.getElementById('operation-create-income-currency').value
    let about = document.getElementById('operation-create-income-about').value
    about = about === "" ? null : about;

    if (accountFrom === '' || accountTo === '' || amount === '') {
        errorCreateIncome.style.display = 'block'
        errorCreateIncome.textContent = 'Введите все данные' // Очистка ошибки, при наличии
        return
    }

    const operationInfo = {
        operation_type: operationType,
        from_account: accountFrom,
        to_account: accountTo,
        amount: amount,
        currency: currency,
        about: about
    };
    const jsonData = JSON.stringify(operationInfo);

    createOperation(jsonData).then(data => {
        if (data.status == 'success') {
            // Операция добавляется в переменную
            addLocalOperation(data.data)

            // Обновление общих раходов и доходов
            updateTotals(operations)

            // Обновление доходов и расходов по категориям
            categoryDict = createCategoryDict(categories, operations)
            updateCategoryTotals(categoryDict)

            // Обновление счета с которого была сделана операция
            updateLocalAccount(accounts, operationInfo)

            // Обновление счетов
            updateAccounts(accounts)

            errorCreateIncome.style.display = 'none'
            closeModal('create-operation-income-modal')
        }
    });
});