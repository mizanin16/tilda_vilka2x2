    // Задаем параметры для исключения параметров. Заполняется Специалистом!
    var excludedItems = ['Хинкали', 'Хинкали с креветками в сливочном соусе и песто', 'Хинкали с говядиной и свининой', 'Хинкали с бараниной', 'Хинкали с сыром сулугуни', 'Хинкали с грибами', 'Стейк по-техасски', 'Тар-тар', 'Шашлык из мякоти баранины', 'Чимичурри', 'Аджика домашняя', 'Ткемали', 'Наршараб', 'Сацебели', 'Чесночный', 'Мацони с зеленью', 'Салат с хрустящими баклажанами', 'Салат нисуаз', 'Теплый салат с куриной печенью', 'Сырные шарики', 'Луковые кольца', 'Пармиджано', 'Паста с белыми грибами и цыпленком', 'Удон с телятиной', 'Свиные ребра BBQ с картофелем по-деревенски', 'Рибай стейк', 'Tvoi burger'
];

    setInterval(verifyAndUpdateCartTotalWithDelay,
2000);

    function checkAndExecute() {
        setTimeout(function() {
            if (typeof window.tcart !== 'undefined' &&
                typeof window.tcart.promocode !== 'undefined' &&
                typeof window.tcart.promocode.discountpercent !== 'undefined') {
                verifyAndUpdateCartTotalWithDelay();
                executeFirstScript();
        } else {
                verifyAndUpdateCartTotalWithDelay();
                checkAndExecute(); // Если промокод не применен, продолжаем проверку
        }
    },
    100); // После выполнения executeFirstScript ждем 100 миллисекунд
}
    
function verifyAndUpdateCartTotalWithDelay() {
    setTimeout(function() {
            if (typeof window.tcart !== 'undefined' &&
                typeof window.tcart.promocode !== 'undefined' &&
                typeof window.tcart.promocode.discountpercent !== 'undefined') {
        var calculatedDiscountedTotal = calculateDiscountForNonExcludedItems(calculateExcludedItemsTotal(excludedItems)).totalWithDiscount;
        if (window.tcart.prodamount_withdiscount !== calculatedDiscountedTotal) {
            console.log("verifyAndUpdateCartTotalWithDelay:");

            executeFirstScript();
            }
        }
    },
    2000);
}

$(document).ready(function() {
    verifyAndUpdateCartTotalWithDelay();


    $(document).on('click', '.t706__product-plus, .t706__product-minus, .t706__product-quantity, .t706__product-del, .t706__product-deleted__timer__return', function() {
        checkAndExecute();
    });


    $('.t-inputpromocode__btn').click(function() {
        setTimeout(function() {
            if (typeof window.tcart !== 'undefined' &&
                typeof window.tcart.promocode !== 'undefined' &&
                typeof window.tcart.promocode.discountpercent !== 'undefined') {
                executeFirstScript();
            } else {
                checkAndExecute(); 
            }
        },
        30);
    });
});


function executeFirstScript() {
    var hasExcludedItems = false;

    // Проверяем наличие исключаемых товаров в корзине
    for (var i = 0; i < window.tcart.products.length; i++) {
        var productName = window.tcart.products[i
        ].name.toLowerCase();
        if (excludedItems.some(item => productName.includes(item.toLowerCase()))) {
            hasExcludedItems = true;
            break;
        }
    }

    if (!hasExcludedItems) return;

    var excludedItemsTotal = calculateExcludedItemsTotal(excludedItems);

    var results = calculateDiscountForNonExcludedItems(excludedItemsTotal);

    var prodamount_withdyndiscount = parseInt(results.totalWithDiscount,
    10);
    var amount = prodamount_withdyndiscount + window.tcart.delivery.price;
    var prodamount_discountsum = parseInt(results.discount,
    10);

    window.tcart.prodamount_withdyndiscount = prodamount_withdyndiscount;
    window.tcart.prodamount_withdiscount = prodamount_withdyndiscount;
    window.tcart.amount = amount;

    window.tcart.prodamount_discountsum = prodamount_discountsum;
    window.tcart.promocode.prodamount_discountsum = prodamount_discountsum;
    tcart__reDrawTotal();

    console.log("Сумма заказа:", window.tcart.amount + "р.");
    console.log("Сумма исключенных товаров:", excludedItemsTotal + "р.");
    console.log("Скидка: " + prodamount_discountsum + "р.");
    console.log("Сумма со скидкой: " + prodamount_withdyndiscount + "р.");
    console.log("Итоговая: " + amount + "р.");
}

function calculateExcludedItemsTotal(excludedItems) {
    var excludedItemsTotal = 0;

    // Рассчитываем общую стоимость исключенных товаров
    for (var i = 0; i < window.tcart.products.length; i++) {
        var productName = window.tcart.products[i
        ].name.toLowerCase();
        var productPriceStr = window.tcart.products[i
        ].amount;
        var productPrice = parseFloat(productPriceStr);
        
        // Если товар не исключен, добавляем его стоимость к исключенным товарам
        if (!excludedItems.some(item => productName.includes(item.toLowerCase()))) {
            excludedItemsTotal += productPrice;
        }
    }

    return excludedItemsTotal;
}

function calculateDiscountForNonExcludedItems(excludedItemsTotal) {
    var discountPercent = parseFloat(window.tcart.promocode.discountpercent); 

    var discount = excludedItemsTotal * (discountPercent  / 100);
    var totalWithDiscount = window.tcart.prodamount - discount;

    return { discount: discount, totalWithDiscount: totalWithDiscount
    };
}




