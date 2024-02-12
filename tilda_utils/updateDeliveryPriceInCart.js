<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>


$(document).ready(function () {
    const apiUrl = 'ADDRESS_API/check-address/';

    const deliveryRadios = document.querySelectorAll('input[name="deliverypoint"]');

    function blockRadios() {
        deliveryRadios.forEach(radio => {
            radio.disabled = true;
        });
    }
    function unblockRadios() {
        deliveryRadios.forEach(radio => {
            radio.disabled = false;
        });
    }
    function checkAddressAndSelectDelivery(address) {
        unblockRadios();
        $.ajax({
            type: 'POST',
            url: apiUrl,
            data: JSON.stringify({
                address: address
            }),
            contentType: 'application/json',
            success: function (response) {

                tcart__reDrawTotal();
                if (response.is_address_in_zone) {
                    const description = response.description;
                    let selectedRadio = null;
                    let deliveryPrice = 0; // Переменная для хранения стоимости доставки

                    if (description.includes('от 1000 руб.')) {
                        selectedRadio = 'Зона 1. Бесплатная доставка';
                    } else if (description.includes('от 1500 руб.')) {
                        selectedRadio = 'Зона 2. Доставка 300 руб. = 300';
                        deliveryPrice = 300; // Устанавливаем стоимость доставки
                    } else if (description.includes('от 3000 руб.')) {
                        selectedRadio = 'Зона 3. Доставка 500 руб. = 500';
                        deliveryPrice = 500; // Устанавливаем стоимость доставки
                    } else {
                        selectedRadio = 'Доставку не осуществляем в выбранный район';
                        alert("Доставку не осуществляем в выбранный район.");
                    }

                    if (selectedRadio) {
                        $('input[value="' + selectedRadio + '"]').prop('checked', true);
                    }
                    // Обновляем стоимость доставки в корзине
                    updateDeliveryPriceInCart(deliveryPrice);
                    tcart__updateDelivery();
                    setTimeout(function () {
                        var requestData = {
                            prodamount: window.tcart.prodamount,
                            discount: window.tcart.discount,
                            products: JSON.stringify(window.tcart.products),
                            amount: window.tcart.amount,
                            total: window.tcart.total,
                            updated: window.tcart.updated
                        };

                        var requestDataJSON = JSON.stringify(requestData);
                        tcart__updateProductsPrice(requestDataJSON);

                        var amount = window.tcart.prodamount_withdiscount + window.tcart.delivery.price;
                        window.tcart.amount = amount;


                        tcart__updateDelivery();
                        tcart__reDrawCartIcon(); // Обновление иконки корзины
                        tcart__reDrawProducts(); // Обновление списка продуктов
                        tcart__reDrawTotal(); // Обновление общей стоимости
                        if (window.tcart.promocode !== undefined) {
                            checkAndExecute();
                        }
                    },
                        100); 
                } else {
                    selectedRadio = 'Доставку не осуществляем в выбранный район';
                    $('input[value="' + selectedRadio + '"]').prop('checked', true);
                $('input[value="Самовывоз"]').prop('checked', true).change(); // выберите Самовывоз и вызовите обработчик change, чтобы очистить поле адреса
                alert("Адрес не входит в зону доставки. \nВведите адрес заново и выберите способ доставки Курьер или выберите Самовывоз");
                }
                blockRadios(); 
            },
            error: function (error) {
                // alert("Ошибка при запросе к серверу. Попробуйте обновить страницу. Если это не поможет, сообщите следующее значение администратору:" + error);
                alert("Ошибка при запросе к серверу. Попробуйте выполнить заказ позже\n" + error);
                $('input[value="Самовывоз"]').prop('checked', true).change(); // выберите Самовывоз и вызовите обработчик change, чтобы очистить поле адреса
            tcart__reDrawTotal();
                console.error("Ошибка при запросе к API:", error);
                selectedRadio = 'Доставку не осуществляем в выбранный район';
                $('input[value="' + selectedRadio + '"]').prop('checked', true);
            blockRadios(); // Заблокировать радиокнопки, если произошла ошибка
            }
        });
    }
    // Функция для обновления стоимости доставки в корзине
    function updateDeliveryPriceInCart(price) {
        window.tcart.delivery = window.tcart.delivery || {};
        window.tcart.delivery.price = price;
        tcart__reDrawTotal(); // Вызывает пересчет и обновление корзины
        const deliveryPriceElement = $('.your-delivery-price-element-selector');
        deliveryPriceElement.hide();
        // Принудительная перерисовка
        deliveryPriceElement.show();
        window.dispatchEvent(new Event('resize'));
        document.addEventListener("DOMContentLoaded", function () {
            var totalsElement = document.querySelector(".t706__cartpage-totals");

            // Функция для изменения класса и вызова обновления
            function togglePinnedClass() {
                if (totalsElement.classList.contains("is-pinned")) {
                    totalsElement.classList.remove("is-pinned");
                } else {
                    totalsElement.classList.add("is-pinned");
                }
                // Вызовите функции для обновления корзины
                tcart__updateTotalProductsinCartObj();
                tcart__reDrawTotal();
                tcart__updateDelivery();
            }
            // Вызовите функцию при изменении размера окна
            window.addEventListener("resize", togglePinnedClass);
        });
    }

    $('input[value="Самовывоз"]').change(function() {
    if ($(this).is(':checked')) {
        let addressInput = $('#input_1678364115361');

        // Разблокировать поле ввода адреса
        addressInput.prop('readonly', false);

        // Очистить поле адреса
        addressInput.val('');
        selectedRadio = 'Доставку не осуществляем в выбранный район';
        $('input[value="' + selectedRadio + '"]').prop('checked', true);
        tcart__updateDelivery();
        if (window.tcart.promocode !== undefined) {
            // Вызываем функцию для выполнения кода из первого скрипта
            checkAndExecute();
        }
    }
});
// Обработчик события для радиокнопки "Курьер"
$('input[value="Курьер"]').change(function() {
        if ($(this).is(':checked')) {
    let addressInput = $('#input_1678364115361');

    // Добавить "Санкт-Петербург" к адресу, если его нет
    let address = addressInput.val();

    // Добавить "Санкт-Петербург" к адресу, если его нет
    if (!address.includes("Санкт-Петербург")) {
        address = "Санкт-Петербург " + address;
    }

    checkAddressAndSelectDelivery(address);
    if (window.tcart.promocode !== undefined) {
        // Вызываем функцию для выполнения кода из первого скрипта
        checkAndExecute();
    }
    // Восстановить атрибут disabled после сбора данных, если нужно
    addressInput.prop('readonly', true);
}
    });


blockRadios(); // Заблокировать радиокнопки при загрузке страницы
});
