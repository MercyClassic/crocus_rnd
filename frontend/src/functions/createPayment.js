import PaymentCreateRequest from '../API/PaymentCreateRequest';


const createPayment = async (event) => {
    event.preventDefault();
    const form = event.target.closest('form');
    const isMobilePhone = (str) => /^\+?[7, 8]-?\s*-?\(?\d{3}\)?-?\s*-?\d{3}-?\s*-?\d{2}-?\s*-?\d{2}$/.test(str);

    if (!form.customer_is_receiver.checked && !form.receiver_phone_number.value) {
        alert('Не заполнена информация о получателе заказа. Если вы являетесь получателем, то нажмите на соответствующую галочку!') ;
        return null;
    }

    if ((isMobilePhone(form.customer_phone_number.value) === false) ||
     (isMobilePhone(form.receiver_phone_number.value) === false)) {
        alert('Телефон не соответствует СНГ формату, убедитесь в том, что номер написан верно');
        return null;
    }

    if(!form.delivery_date.value) {
        alert('Укажите дату доставки/самовывоза');
        return null
    }

    let items = {};
    const amount = form.querySelector('.popup-cart__price').dataset.amount;
    let counters = document.querySelectorAll('[data-counter]');

    if (counters === undefined) {
        alert('Для заказа в корзине должен находиться хотя бы один товар');
        return null;
    }

    if (!form.cash.checked && !form.email.value) {
        alert('При оплате онлайн укажите адрес электронной почты');
        return null;
    }

    counters.forEach(counter => {
        let el = counter.querySelector('input');
        items[el.dataset.slug] = el.value;
    });

    const data = {
        'items': items,
        'amount': amount,
        'customer_name': form.customer_name.value,
        'receiver_name': form.receiver_name.value,
        'customer_phone_number': form.customer_phone_number.value,
        'receiver_phone_number': form.receiver_phone_number.value,
        'without_calling': form.without_calling.checked,
        'customer_email': form.email.value,
        'delivery_address': form.delivery_address.value,
        'delivery_date': form.delivery_date.value,
        'delivery_time': form.delivery_time.value,
        'note': form.note.value,
        'cash': form.cash.checked,
        'delivering': form.delivering.checked,
        'promo_code': form.promo_code.value
    }

    await PaymentCreateRequest(data).then((response) => {
        if (response.status === 201) {
            if (response.data.payment_url === 'OK') {
                alert('Ваш заказ успешно оформлен, начинаем его собирать!');
                window.location.href = '/';
            } else {
		        window.open(response.data.payment_url, "_blank");
            }
        } else if (response.status === 400) {
            alert(JSON.parse(response.responseText));
        } else if (response.status === 403) {
            alert(JSON.parse(response.responseText));
        } else if (response.status === 500) {
            alert('Произошла ошибка на стороне сервера, попробуйте обновить страничку и повторить заказ снова');
        }
    })
}

export default createPayment;
