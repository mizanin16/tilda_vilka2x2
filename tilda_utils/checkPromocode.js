function waitForPromoCodeInput() {
    const promoCodeInput = document.querySelector('.t-inputpromocode');
    if (promoCodeInput) {
        // Если поле ввода промокода найдено, продолжаем
        setPromoCode(promoCodeInput);
    } else {
        setTimeout(function() {
            waitForPromoCodeInput(); // Рекурсивный вызов функции
        }, 1000);
    }
}

function setPromoCode(inputElement) {
    let projectId = parseInt(document.querySelector('#allrecords').dataset.tildaProjectId);
    let lsUser = window.localStorage.getItem('tilda_members_profile' + projectId);
    let userEmail = lsUser != null ? JSON.parse(lsUser).login : false;

    if (userEmail) {
        // Если есть email пользователя, делаем AJAX-запрос на сервер Django
        let apiUrl = 'ADDRESS_API//?email=' + encodeURIComponent(userEmail);

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Проверяем ответ сервера на наличие промокода
                if (data.status === 'success' && data.promocode) {
                    // Если промокод получен, вставляем его в поле ввода
                    inputElement.value = data.promocode;
                    // Создаем и инициализируем событие "input", чтобы активировать обработчики изменения поля ввода
                    let inputEvent = new Event('input', {
                        bubbles: true,
                        cancelable: true,
                    });
                    inputElement.dispatchEvent(inputEvent);

                    const activateButton = document.querySelector('.t-inputpromocode__btn');

                    // Показываем кнопку "Активировать" при загрузке страницы
                    activateButton.style.display = 'block';

                }
            })
            .catch(error => {
                console.error("Ошибка при запросе к API:", error);
            });
    }
}

// Вызываем waitForPromoCodeInput один раз при загрузке страницы
waitForPromoCodeInput();
