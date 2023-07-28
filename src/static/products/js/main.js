// FUNCTIONS


function addToSession(event) {
    event.preventDefault();
    let type;
    if (event.target.name === 'form-add-to-cart') {
        type = 'cart';
    }
    else if (event.target.name === 'form-add-to-favourite') {
        type = 'favourite';
    }
    const url = event.target.action;
    const csrf_token = event.target.csrfmiddlewaretoken.value;
    postData(url, data={'type': type}, csrf=csrf_token)
    .then((response) => {
        if (response.status === 201) {
            if (type === 'favourite') {
                event.target.like_button.innerHTML = `<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
                                         width="27.000000pt" height="27.000000pt" viewBox="0 0 1280.000000 1248.000000"
                                         preserveAspectRatio="xMidYMid meet">
                                            <g transform="translate(0.000000,1248.000000) scale(0.100000,-0.100000)"
                                            fill="#f44336" stroke="none">
                                                <path d="M2860 11344 c-19 -2 -80 -9 -135 -15 -680 -71 -1336 -412 -1794 -933
                                                -381 -434 -661 -983 -826 -1621 -342 -1324 170 -2767 1549 -4365 342 -396 875
                                                -927 1361 -1356 705 -622 1556 -1266 2365 -1790 218 -142 414 -264 423 -264
                                                20 0 519 323 841 544 1779 1224 3216 2581 4038 3816 533 800 837 1566 908
                                                2288 14 149 15 491 0 622 -27 257 -88 526 -181 804 -192 575 -457 1033 -808
                                                1398 l-114 119 34 37 c31 34 31 35 4 12 -16 -14 -33 -29 -37 -34 -3 -5 -49 27
                                                -102 71 -52 45 -105 88 -116 96 -18 12 -19 18 -10 42 6 15 8 30 6 33 -3 2 -8
                                                -7 -12 -22 -3 -14 -9 -26 -12 -26 -3 0 -37 22 -76 49 -379 260 -774 410 -1256
                                                478 -173 24 -583 24 -765 0 -515 -69 -982 -241 -1390 -513 -431 -287 -749
                                                -666 -915 -1090 -22 -57 -41 -93 -44 -84 -46 125 -64 169 -112 264 -244 487
                                                -713 907 -1304 1169 -282 124 -583 208 -910 252 -109 15 -532 28 -610 19z"/>
                                                <path d="M10728 10363 c7 -3 16 -2 19 1 4 3 -2 6 -13 5 -11 0 -14 -3 -6 -6z"/>
                                            </g>
                                        </svg>`
            } else {
                if (event.target.hasAttribute('data-product-detail')) {
                        event.target.add_to_cart_button.classList.remove('product-content__add-button');
                        event.target.add_to_cart_button.classList.add('product-content__delete-button');
                        event.target.add_to_cart_button.innerHTML = 'Удалить из корзины';
                } else {
                    event.target.add_to_cart_button.innerHTML = `<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                                             width="64px" height="64px" viewBox="0 0 64 64" enable-background="new 0 0 64 64" xml:space="preserve">
                                            <g>
                                            <path d="M52.728,60H11.272L-0.375,24h64.749L52.728,60z M12.728,58h38.545l10.353-32H2.375L12.728,58z"/>
                                            </g>
                                            <g>
                                            <rect x="17" y="4.23" transform="matrix(0.9284 0.3715 -0.3715 0.9284 6.8601 -5.6132)" width="2.001" height="21.541"/>
                                            </g>
                                            <g>
                                            <rect x="35.23" y="14" transform="matrix(0.3714 0.9285 -0.9285 0.3714 42.8432 -33.2808)" width="21.541" height="2.001"/>
                                            </g>
                                            <g>
                                            <polygon points="30.707,48.707 29.293,48.707 22.293,41.707 23.707,40.293 30,46.586 42.293,34.293 43.707,35.707 	"/>
                                            </g></svg>`
                    }
                let count_cart_products = document.querySelector('.icon-cart__count');
                count_cart_products.innerHTML = Number(count_cart_products.innerHTML) + 1;
            }
        } else {
            if (type === 'favourite') {
                event.target.like_button.innerHTML = `<svg width="36px" height="36px" viewBox="0 0 24 24" fill="none"
                                            xmlns="http://www.w3.org/2000/svg">
                                            <path
                                                d="M12 20L4.3314 12.0474C3.47892 11.1633 3 9.96429 3 8.71405C3 6.11055 5.03517 4 7.54569 4C8.75128 4 9.90749 4.49666 10.76 5.38071L12 6.66667L13.24 5.38071C14.0925 4.49666 15.2487 4 16.4543 4C18.9648 4 21 6.11055 21 8.71405C21 9.96429 20.5211 11.1633 19.6686 12.0474L15.8343 16.0237"
                                                stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                                        </svg>`
            } else {
                if (event.target.hasAttribute('data-product-detail')) {
                        event.target.add_to_cart_button.classList.remove('product-content__delete-button');
                        event.target.add_to_cart_button.classList.add('product-content__add-button');
                        event.target.add_to_cart_button.innerHTML = 'Добавить в козину';
                    } else {
                        event.target.add_to_cart_button.innerHTML = `<svg height="64" width="64" xmlns="http://www.w3.org/2000/svg" viewBox="2 0 30 27">
                                                    <path d="M1.39999 1.70001H6.60001" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M6.60001 1.70001L11 18.9" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M11.8 18.9H28.3" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M13.8 25.7C15.4569 25.7 16.8 24.3569 16.8 22.7C16.8 21.0432 15.4569 19.7 13.8 19.7C12.1431 19.7 10.8 21.0432 10.8 22.7C10.8 24.3569 12.1431 25.7 13.8 25.7Z" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M25.3 25.7C26.9568 25.7 28.3 24.3569 28.3 22.7C28.3 21.0432 26.9568 19.7 25.3 19.7C23.6431 19.7 22.3 21.0432 22.3 22.7C22.3 24.3569 23.6431 25.7 25.3 25.7Z" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M25.7 14.6H11.3C10.7 14.6 10.1 14.2 10 13.6L8.1 6.90001C7.9 6.00001 8.49999 5.20001 9.39999 5.20001H27.5C28.4 5.20001 29.1 6.10001 28.8 6.90001L26.9 13.6C26.9 14.2 26.4 14.6 25.7 14.6Z" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                </svg>`
                        }
                let count_cart_products = document.querySelector('.icon-cart__count');
                count_cart_products.innerHTML = Number(count_cart_products.innerHTML) - 1;

            }
        }
    });
}


const postData = async (url = '', data={}, csrf = '') => {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf
    },
    body: JSON.stringify(data)
  });
  return response;
}


const getData = async (url = '') => {
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.json();
}


function getCart(event) {
    event.preventDefault();
    let cart_wrapper = document.getElementById('cart_wrapper')
    if (cart_wrapper.classList.contains('non_visible')) {
        cart_wrapper.classList.remove('non_visible')
    }
    if (cart_wrapper.getAttribute('data-oneclick') !== null) {
        cart_wrapper.removeAttribute('data-oneclick')
    }
    let cart_items = document.getElementById('cart_items');
    let tags = '';
    let amount = 0;
    getData(cart.href)
    .then((data) => {
        data.forEach(product => {
              tags += `<li class="popup-cart__item popup-item-cart" id=product_${product.slug}>
                            <div class="popup-item-cart__image-wrapper">
                                <img src=${product.image} alt="Icon">
                            </div>
                            <h6 class="popup-item-cart__title"><a href=${product.url}> ${product.title} </a></h6>
                            <div name="price">${product.price}₽</div>
                            <div class="popup-item-cart__count-block" data-counter>
                                <div class="popup-item-cart__minus-button" data-action='minus'>
                                    <span></span>
                                </div>
                                <input id=${product.slug} class="popup-item-cart__input" type="text" value="1" disabled>
                                <div class="popup-item-cart__plus-button" data-action='plus'>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </li>`
              amount += Number(product.price)
        })
    if (!tags) {
        cart_items.innerHTML = 'Корзина пуста'
    } else {
        cart_items.innerHTML = tags;
        document.getElementById('amount').innerHTML = `Сумма: ${amount} ₽`
        document.getElementById('amount').setAttribute('data-amount', amount)
    }
    });
}


function getOneClickPaymentForm(event) {
    event.preventDefault();
    let cart_wrapper = document.getElementById('cart_wrapper')
    if (cart_wrapper.classList.contains('non_visible')) {
        cart_wrapper.classList.remove('non_visible')
    }
    if (cart_wrapper.getAttribute('data-oneclick') === null) {
        cart_wrapper.setAttribute('data-oneclick', true)
    }
    let price = document.querySelector('.product-content__price').getAttribute('data-price');
    let title = document.querySelector('.product-content__title');
    let cart_items = document.getElementById('cart_items');
    cart_items.innerHTML = `<li class="popup-cart__item popup-item-cart">
                            <div class="popup-item-cart__image-wrapper">
                                <img src=${document.querySelector('.main-product__image-wrapper').querySelector('img').src} alt="Icon">
                            </div>
                            <h6 class="popup-item-cart__title"><a href=${'sss'}> ${title.innerHTML} </a></h6>
                            <div name="price">${price}₽</div>
                            <div class="popup-item-cart__count-block" data-counter>
                                <div class="popup-item-cart__minus-button" data-action='minus'>
                                    <span></span>
                                </div>
                                <input id=${title.getAttribute('data-slug')} class="popup-item-cart__input" type="text" value="1" disabled>
                                <div class="popup-item-cart__plus-button" data-action='plus'>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </li>`
    document.getElementById('amount').innerHTML = `Сумма: ${price} ₽`
    document.getElementById('amount').setAttribute('data-amount', price)
    let counters = document.querySelectorAll('[data-counter]');
}


const setCount = function(counters) {
    counters.forEach(counter => {
        counter.addEventListener('click', event => {
            let target = event.target;
            if (target.tagName === 'SPAN') {
                target = target.parentNode
            }
            if (target.closest('.popup-item-cart__count-block')) {
                let value = parseInt(target.closest('.popup-item-cart__count-block').querySelector('input').value);
                if (target.closest('[data-action]').getAttribute('data-action') === 'plus') {
                    value++;
                } else {
                    --value;
                }

                if (value !== 0) {
                    result = changeAmount(target);
                    if (result === false) {--value}
                }

                if (value < 1) {
                    delete_from_cart(target);
                    value = 1;
                    target.closest('.popup-item-cart__count-block').querySelector('.popup-item-cart__plus-button').classList.add('disabled');
                } else {
                    target.closest('.popup-item-cart__count-block').querySelector('.popup-item-cart__minus-button').classList.remove('disabled');
                }

                target.closest('.popup-item-cart__count-block').querySelector('input').value = value;
            }
        })
    })
}


function createPayment(event) {
    event.preventDefault();
    let target = event.target.closest('form');
    const isMobilePhone = (str) => /^\+?[7, 8]\s*\(?\d{3}\)?\s*\d{3}-?\d{2}-?\d{2}$/.test(str);
    if ((isMobilePhone(target.customer_phone_number.value) === false) ||
     (isMobilePhone(target.receiver_phone_number.value) === false)){
        alert('Телефон не соответствует СНГ формату, убедитесь в том, что номер написан верно');
        return null;
    }
    let items = {};
    if (target.getAttribute('data-oneclick') !== null) {
        let slug = document.querySelector('.product-content__title').getAttribute('data-slug');
        items[slug] = counters[0].querySelector('input').value;
    } else {
        let counters = document.querySelectorAll('[data-counter]');
        if (counters) {
           setCount(counters);
        }
        if (counters === undefined) {
            alert('Для заказа в корзине должен находиться хотя бы один товар');
            return null;
        }
        counters.forEach(counter => {
            el = counter.querySelector('input');
            items[el.id] = el.value;
        });
    }
    data={
        'items': items,
        'amount': document.getElementById('amount').getAttribute('data-amount'),
        'customer_name': target.customer_name.value,
        'receiver_name': target.receiver_name.value,
        'customer_phone_number': target.customer_phone_number.value,
        'receiver_phone_number': target.receiver_phone_number.value,
        'without_calling': document.getElementById('without_calling').checked,
        'delivery_address': target.delivery_address.value,
        'delivery_date': target.delivery_date.value,
        'delivery_time': target.querySelector('.popup-cart__time-input').value,
        'note': target.note.value,
        'delivering': document.getElementById('delivering').checked
    }

    showLoader(true);
    postData(
        url=target.action,
        data=data,
        csrf=target.csrfmiddlewaretoken.value
    ).then((response) => {
        if (response.status === 201) {
            response.json()
            .then((data) => {
		alert('Онлайн оплата временно недоступна, свяжитесь с нами напрямую');
		return null;
                // window.open(data.payment_url);
           })
        } else if (response.status === 400) {
            alert('Данные введены неверно, обновите страничку и попробуйте ещё раз')
        } else if (response.status === 500) {
            alert('Произошла ошибка на стороне сервера, попробуйте обновить страничку и повторить заказ снова')
        } else if (response.status === 403) {
            alert('Вы уже сделали заказ, подождите немного, прежде, чем сделать ещё один')
        }
        showLoader(false);
    })
}


function isWithDeliver(event) {
    const amount = document.getElementById('amount');
    let disabled_cart_inputs = document.querySelectorAll('[data-disable-before-delivery-checked]');
    if (event.target.checked) {
        result = Number(amount.getAttribute('data-amount')) + 350;
        amount.setAttribute('data-amount', result);
        amount.innerHTML = `Сумма: ${result} ₽`;
        disabled_cart_inputs.forEach((input) => {input.removeAttribute('disabled')});
        document.querySelector('.popup-cart__delivery-price').innerHTML = 'Доставка: 350 ₽';
    } else {
        result = Number(amount.getAttribute('data-amount')) - 350;
        amount.innerHTML = `Сумма: ${result} ₽`;
        amount.setAttribute('data-amount', result);
        disabled_cart_inputs.forEach((input) => {input.setAttribute('disabled', true)});
        document.querySelector('.popup-cart__delivery-price').innerHTML = 'Доставка: 0 ₽';
    }
    document.querySelector('.popup-cart__last-price').innerHTML = `Итоговая сумма: ${result} ₽`;
}


function changeAmount(target) {
    const amount = document.getElementById('amount');
    const last_price = document.querySelector('.popup-cart__last-price');
    const price = Number(target.parentNode.parentNode.children.price.innerHTML.slice(0, -1));
    let result = 0;
    if (target.dataset.action === 'plus') {
        result = Number(amount.getAttribute('data-amount')) + price;
        if (result > 50000) {
            alert('Для заказа свыше 50 000 рублей, свяжитесь с продавцом');
            return false;
        } else {
            amount.setAttribute('data-amount', result);
            amount.innerHTML = `Сумма: ${result} ₽`;
            if (last_price !== null) {
                last_price.innerHTML = `Сумма: ${result} ₽`;
            }
        }
    } else if (target.dataset.action === 'minus') {
        result = Number(amount.getAttribute('data-amount')) - price;
        amount.innerHTML = `Сумма: ${result} ₽`;
        if (last_price !== null) {
            last_price.innerHTML = `Сумма: ${result} ₽`;
        }
        amount.setAttribute('data-amount', result)
    }
}


function showLoader(bool) {
    if (bool === true) {
        const mask = document.createElement('div');
        mask.setAttribute('class', 'mask');
        document.body.appendChild(mask);
        const loader = document.createElement('div');
        loader.setAttribute('class', 'loader');
        mask.appendChild(loader);
    } else {
        const mask = document.querySelector('.mask');
        mask.remove();
    }
}


function closeCart(event) {
    const c = document.getElementById('cart_wrapper');
    c.classList.add('non_visible');
    document.getElementById('after_continue').innerHTML = '';
    continue_payment_div = document.querySelector('.popup-cart__next-button-wrapper');
    if (continue_payment_div.querySelector('button') === null) {
        continue_payment_div.innerHTML = `<button type="button" class="popup-cart__next-button _black-button">Продолжить</button>`;
        continue_payment_button = document.querySelector('.popup-cart__next-button');
        continue_payment_button.addEventListener('click', continuePayment);
    }
}


function customerIsReceiver(event) {
    let div_after_continue  = form_create_payment.children.after_continue;
    let customer_name = form_create_payment.querySelector('.popup-cart__name-input');
    let customer_phone_number = form_create_payment.querySelector('.popup-cart__phone-input');
    let receiver_name = div_after_continue.querySelector('.popup-cart__name-input');
    let receiver_phone_number = div_after_continue.querySelector('.popup-cart__phone-input');
    if (event.target.checked) {
        receiver_name.value = customer_name.value;
        receiver_phone_number.value = customer_phone_number.value;
        receiver_name.setAttribute('disabled', true)
        receiver_phone_number.setAttribute('disabled', true)
    } else {
        receiver_name.removeAttribute('disabled')
        receiver_phone_number.removeAttribute('disabled')
    }
}


function continuePayment(event) {
    let name = document.querySelector('.popup-cart__name-input');
    let phone = document.querySelector('.popup-cart__phone-input');
    if (name.value === '' || phone.value === '') {
        alert('Для начала введите имя и номер телефона');
        return null;
    }
    let amount = document.getElementById('amount').getAttribute('data-amount');
    document.getElementById('after_continue').innerHTML =
                        `<div class="popup-cart__adress-lable _label">
			    <label class="popup-cart__date-label _label">Адрес доставки <p> <span style="font-size:14px">(Выберите пункт "С доставкой" для редактирования)<span></p></label>
			</div>
                        <input name='delivery_address' data-disable-before-delivery-checked type="text" disabled placeholder="Пример: ул. Пушкинская 4" class="popup-cart__adress-input _input">
                        <div class="popup-cart__date-wrapper">
                            <label class="popup-cart__date-label _label">Дата доставки / Самовывоза </label>
                            <input name='delivery_date' type="date" required class="popup-cart__date-input _input">
                        </div>
                        <div class="popup-cart__time-wrapper">
                            <label name='delivery_time' class="popup-cart__time-label _label">Время доставки <br><span style="font-size:14px">(Выберите пункт "С доставкой" для редактирования)<span></label>
                            <input data-disable-before-delivery-checked type="text" disabled placeholder="Пример: с 10:00 до 11:00" class="popup-cart__time-input _input">
                        </div>
                        <div class="popup-cart__checkbox-wrapper">
                            <input type="checkbox" id="customer_is_receiver" class="popup-cart__checkbox-input">
                            <label name="customer_is_receiver" class="popup-cart__chekbox-label">Заказчик является получателем заказа</label>
                        </div>
                         <div class="popup-cart__input-name-wrapper">
                            <label class="popup-cart__name-label _label">Имя получателя</label>
                            <input type="text" class="popup-cart__name-input _input" name="receiver_name" placeholder="Введите имя получателя" required maxlength="50" minlength="2">
                        </div>
                        <div class="popup-cart__input-phone-wrapper">
                            <label class="popup-cart__phone-label _label">Телефон получателя</label>
                            <input type="text" placeholder="Например: +7 (999) 777-77-77" class="popup-cart__phone-input _input" name="receiver_phone_number" required maxlength="20" minlength="11">
                        </div>
                        <div class="popup-cart__checkbox-wrapper">
                            <input type='checkbox' id='delivering' class="popup-cart__checkbox-input">
                            <label class="popup-cart__chekbox-label"> С доставкой (+350 рублей) </label>
                        </div>
                        <div class="popup-cart__checkbox-wrapper">
                            <input type='checkbox' id='without_calling' class="popup-cart__checkbox-input">
                            <label class="popup-cart__chekbox-label"> Напишите мне в whatsapp/telegram (Не звонить) </label>
                        </div>
                        <div class="popup-cart__input-name-wrapper">
                            <label class="popup-cart__name-label _label">Примечание</label>
                            <textarea class="textarea_note" placeholder="Напишите примечание, если оно требуется" name="note" maxlength=300></textarea>
                        </div>
                        <div class="popup-cart__product-price">Сумма без учёта доставки: ${amount} ₽</div>
                        <div class="popup-cart__delivery-price">Доставка: 0 ₽</div>
                        <div class="popup-cart__last-price">Итоговая сумма: ${amount} ₽ </div>
                        <div class="popup-cart__create-order-button-wrapper">
                            <button type="submit" class="popup-cart__create-order-button _black-button">Оформить заказ</button>
                        </div>`;
    create_payment_button = document.querySelector('.popup-cart__create-order-button')
    create_payment_button.addEventListener('click', createPayment)
    event.target.remove();
    document.getElementById('delivering').addEventListener('click', isWithDeliver);
    customer_is_receiver = document.getElementById('customer_is_receiver');
    customer_is_receiver.addEventListener('click', customerIsReceiver);
    receiver_phone_number = document.getElementsByName('receiver_phone_number')[0];
    receiver_phone_number.addEventListener('click', FormatPhoneNumber);
}


function delete_from_cart(target) {
    postData(
        `add_to_session/${target.parentNode.querySelector('input').id}/`,
        data={'type': 'cart'},
        csrf_token=document.querySelector('.popup-cart__form').csrfmiddlewaretoken.value
    )
    let deleted = target.parentNode.parentNode;
    let deleted_slug = deleted.id.slice(8);
    deleted.remove();
    forms_add_to_cart.forEach((form) => {
        if (form.getAttribute('action') === `/add_to_session/${deleted_slug}/`) {
            form.add_to_cart_button.innerHTML = `<svg height="64" width="64" xmlns="http://www.w3.org/2000/svg" viewBox="2 0 30 27">
                                                    <path d="M1.39999 1.70001H6.60001" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M6.60001 1.70001L11 18.9" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M11.8 18.9H28.3" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M13.8 25.7C15.4569 25.7 16.8 24.3569 16.8 22.7C16.8 21.0432 15.4569 19.7 13.8 19.7C12.1431 19.7 10.8 21.0432 10.8 22.7C10.8 24.3569 12.1431 25.7 13.8 25.7Z" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M25.3 25.7C26.9568 25.7 28.3 24.3569 28.3 22.7C28.3 21.0432 26.9568 19.7 25.3 19.7C23.6431 19.7 22.3 21.0432 22.3 22.7C22.3 24.3569 23.6431 25.7 25.3 25.7Z" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                    <path d="M25.7 14.6H11.3C10.7 14.6 10.1 14.2 10 13.6L8.1 6.90001C7.9 6.00001 8.49999 5.20001 9.39999 5.20001H27.5C28.4 5.20001 29.1 6.10001 28.8 6.90001L26.9 13.6C26.9 14.2 26.4 14.6 25.7 14.6Z" stroke="#4F4F4F" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/>
                                                </svg>`
        }
    })
}


function changeMainPicture(event) {
    let img = document.querySelector('.main-product__image-wrapper').querySelector('img');
    img.setAttribute('src', event.target.getAttribute('src'));
}


function CallMe(event) {
    event.preventDefault();
    const isMobilePhone = (str) => /^\+?[7, 8]\s*\(?\d{3}\)?\s*\d{3}-?\d{2}-?\d{2}$/.test(str);
    if (isMobilePhone(event.target.phone_number.value) === false) {
        alert('Телефон не соответствует СНГ формату, убедитесь в том, что номер написан верно');
        return null;
    }
    showLoader(true);
    postData(
        url=event.target.action,
        data={'phone_number': event.target.phone_number.value},
        csrf=event.target.csrfmiddlewaretoken.value
    ).then((response) => {
        if (response.status === 200) {
            response.json()
            .then((data) => {
                alert(data)
           })
        } else if (response.status === 400) {
            alert('Данные введены неверно, обновите страничку и попробуйте ещё раз')
        } else if (response.status === 403) {
            response.json()
            .then((data) => alert(data))
        } else if (response.status === 500) {
            alert('Произошла ошибка на стороне сервера, попробуйте обновить страничку и повторить заказ снова')
        }
        showLoader(false);
    })
}


function FormatPhoneNumber(event) {
    if (event.target.value === '') {
        event.target.value = '+7';
    }
}


window.addEventListener('load', function(event) {
    let catalog = document.getElementById('catalog');
    if (catalog !== null) {
        if (window.location.href.includes('&catalog')) {
            let url = window.location.href.replace('&catalog', '');
            window.history.replaceState(null, null, url);
            catalog.scrollIntoView({behavior: 'smooth'});
        }
    }
});

// consts


const forms_add_to_cart=document.getElementsByName('form-add-to-cart');
if (forms_add_to_cart !== null) {
    forms_add_to_cart.forEach((form) => form.addEventListener('submit', addToSession));
}


const forms_add_to_favourite=document.getElementsByName('form-add-to-favourite');
if (forms_add_to_favourite !== null) {
    forms_add_to_favourite.forEach((form) => form.addEventListener('submit', addToSession));
}


let cart = document.getElementById('cart');
if (cart !== null) {
    cart.addEventListener('click', getCart);
}


let cart_close_button = document.getElementById('cart_close_button');
if (cart_close_button !== null) {
    cart_close_button.addEventListener('click', closeCart);
}


let payment_continue_button = document.querySelector('.popup-cart__next-button');
if (payment_continue_button !== null) {
    payment_continue_button.addEventListener('click', continuePayment);
}


let product_detail_sliders = document.querySelectorAll('.main-product__slider-image-wrapper');
if (product_detail_sliders !== null) {
    product_detail_sliders.forEach((slider) => slider.addEventListener('click', changeMainPicture));
}


let buy_by_one_click_button = document.getElementById('buy_by_one_click_button');
if (buy_by_one_click_button !== null) {
    buy_by_one_click_button.addEventListener('click', getOneClickPaymentForm)
}


let form_call_me = document.getElementById('call_me');
if (form_call_me !== null) {
    form_call_me.addEventListener('submit', CallMe)
}


let customer_phone_number_input = document.getElementsByName('customer_phone_number')[0];
if (customer_phone_number_input !== null) {
    customer_phone_number_input.addEventListener('click', FormatPhoneNumber);
}


let call_me_input = document.querySelector('.delivery__number-input');
if (call_me_input !== null) {
    call_me_input.addEventListener('click', FormatPhoneNumber);
}


//const mask = document.querySelector('.mask')
//window.addEventListener('load', () => {
//    mask.classList.add('hide');
//    setTimeout(() => {
//        mask.remove();
//    }, 600);
//});


var isMobile = { Android: function () { return navigator.userAgent.match(/Android/i); }, BlackBerry: function () { return navigator.userAgent.match(/BlackBerry/i); }, iOS: function () { return navigator.userAgent.match(/iPhone|iPad|iPod/i); }, Opera: function () { return navigator.userAgent.match(/Opera Mini/i); }, Windows: function () { return navigator.userAgent.match(/IEMobile/i); }, any: function () { return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows()); } };

function _removeClasses(el, class_name) {
	for (var i = 0; i < el.length; i++) {
		el[i].classList.remove(class_name);
	}
}


window.addEventListener('load', () => {
    document.getElementById('current_year').innerHTML = new Date().getFullYear()
})


click()
function click() {
	document.addEventListener("click", documentActions);

	function documentActions(e) {
		const targetElement = e.target;
		if (window.innerWidth > 1200 && isMobile.any()) {
			if (targetElement.classList.contains('menu__link')) {
				targetElement.closest('.menu__item').classList.toggle('_hover');
			}
		}
		if (targetElement.classList.contains('icon-menu')) {
			document.querySelector('.wrapper').classList.toggle('_active');
			document.querySelector('.icon-menu').classList.toggle('_active');
			document.querySelector('.menu').classList.toggle('_active');
			document.querySelector('.actions__tel').classList.toggle('_active');
		}
	}
}
