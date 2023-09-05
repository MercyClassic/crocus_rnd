import {useState} from 'react';
import createPayment from '../functions/createPayment';
import formatPhoneNumber from '../functions/formatPhoneNumber';
import setReceiver from '../functions/setReceiver';


const FullPaymentForm = ({form, amount, setAmount}) => {
    const [delivering, setDelivering] = useState(0);

    form.querySelector('.popup-cart__next-button-wrapper').hidden = true;

    const changeDeliveringPrice = (event) => {
        const form = event.target.closest('form');
        const disabledCartInputs = [form.delivery_address, form.delivery_time];
        if (form.delivering.checked) {
            setDelivering(350);
            amount += 350;
            disabledCartInputs.forEach((input) => {input.removeAttribute('disabled')});
        } else {
            setDelivering(0);
            amount -= 350;
            disabledCartInputs.forEach((input) => {input.setAttribute('disabled', true)});
        }
        setAmount(amount);
    }

    return(
        <>
        <div class="popup-cart__input-email-wrapper">
            <label class="popup-cart__email-label _label">
            Email
            <p>
                <span style={{fontSize: "14px"}}>
                    (Для отправки чека на email)
                </span>
            </p>
            </label>
            <input type="text" name='email' placeholder="Без указания почты чек прикрепляется к букету" class="popup-cart__email-input _input" />
        </div>
        <div className="popup-cart__address-label _label">
            <label className="popup-cart__date-label _label">
                Адрес доставки
                <p>
                    <span style={{fontSize: "14px"}}>
                        (Выберите пункт "С доставкой" для редактирования)
                    </span>
                </p>
            </label>
            <input name='delivery_address' type="text" disabled placeholder="Пример: ул. Пушкинская 4" className="popup-cart__address-input _input" />
        </div>
        <div className="popup-cart__date-wrapper">
            <label className="popup-cart__date-label _label">Дата доставки / Самовывоза </label>
            <input name='delivery_date' type="date" required className="popup-cart__date-input _input" />
        </div>
        <div className="popup-cart__time-wrapper">
            <label className="popup-cart__time-label _label">
                Время доставки
                <p>
                    <span style={{fontSize: "14px"}}>
                        (Выберите пункт "С доставкой" для редактирования)
                    </span>
                </p>
            </label>
            <input name='delivery_time' type="text" disabled placeholder="Пример: с 10:00 до 11:00" className="popup-cart__time-input _input" />
        </div>
        <div className="popup-cart__checkbox-wrapper">
            <label className="popup-cart__checkbox-label">
                <input onClick={(e) => setReceiver(e.target.closest('form'))} type="checkbox" name="customer_is_receiver" className="popup-cart__checkbox-input" />
                Заказчик является получателем заказа
            </label>
        </div>
         <div className="popup-cart__input-name-wrapper">
            <label className="popup-cart__name-label _label">Имя получателя</label>
            <input type="text" className="popup-cart__name-input _input" name="receiver_name" placeholder="Введите имя получателя" required maxLength="50" minLength="2" />
        </div>
        <div className="popup-cart__input-phone-wrapper">
            <label className="popup-cart__phone-label _label">Телефон получателя</label>
            <input type="text" onClick={(e) => formatPhoneNumber(e)} placeholder="Например: +7 (999) 777-77-77" className="popup-cart__phone-input _input" name="receiver_phone_number" required maxLength="20" minLength="11" />
        </div>
        <div className="popup-cart__checkbox-wrapper">
            <label className="popup-cart__checkbox-label">
                <input onClick={(e) => changeDeliveringPrice(e)} type='checkbox' name="delivering" className="popup-cart__checkbox-input" />
                    С доставкой (+350 рублей)
             </label>
        </div>
        <div className="popup-cart__checkbox-wrapper">
            <label className="popup-cart__checkbox-label">
                <input type='checkbox' name='cash' className="popup-cart__checkbox-input" />
                Оплатить наличными при получении
            </label>
        </div>
        <div className="popup-cart__checkbox-wrapper">
            <label className="popup-cart__checkbox-label">
                <input type='checkbox' name='without_calling' className="popup-cart__checkbox-input" />
                <span> Напишите мне в whatsapp/telegram (Не звонить) </span>
             </label>
        </div>
        <div className="popup-cart__input-name-wrapper">
            <label className="popup-cart__name-label _label">Примечание</label>
            <textarea className="textarea_note" placeholder="Напишите примечание, если оно требуется" name="note" maxLength="300"></textarea>
        </div>
        <div className="popup-cart__product-price">Сумма без учёта доставки: {amount - delivering} ₽</div>
        <div className="popup-cart__delivery-price">Доставка: {delivering} ₽</div>
        <div className="popup-cart__last-price">Итоговая сумма: {amount} ₽ </div>
        <div className="popup-cart__create-order-button-wrapper">
            <button onClick={(e) => createPayment(e)} className="popup-cart__create-order-button _black-button">Оформить заказ</button>
        </div>
        </>
    );
}

export default FullPaymentForm;
