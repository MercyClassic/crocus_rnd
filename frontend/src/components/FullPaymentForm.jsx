import {useState} from 'react';
import createPayment from '../functions/createPayment';
import formatPhoneNumber from '../functions/formatPhoneNumber';
import setReceiver from '../functions/setReceiver';
import SetPromoCodeRequest from "../API/SetPromoCodeRequest";
import {Link} from "react-router-dom";


const FullPaymentForm = ({form, amount, setAmount}) => {
    const [delivering, setDelivering] = useState(0);
    const [promoCodeState, setPromoCodeState] = useState(false);

    form.querySelector('.popup-cart__next-button-wrapper').hidden = true;

    const changeDeliveringPrice = (event) => {
        const form = event.target.closest('form');
        const disabledCartInputs = [form.delivery_address, form.delivery_time];
        if (form.delivering.checked) {
            setDelivering(450);
            amount += 450;
            disabledCartInputs.forEach((input) => {input.removeAttribute('disabled')});
        } else {
            setDelivering(0);
            amount -= 450;
            disabledCartInputs.forEach((input) => {input.setAttribute('disabled', true)});
            form.delivery_address.value = '';
        }
        setAmount(amount);
    }

    const setPromoCode = async (event) => {
        event.preventDefault();
        const form = event.target.closest('form');
        if (promoCodeState) {
            alert('Вы уже применили промокод!')
        } else if (form.promo_code.value) {
            let promo_amount = amount
            if (delivering) {
                promo_amount -= 450
            }
            const data = {
                'promo_code': form.promo_code.value,
                'amount': promo_amount,
            }
            await SetPromoCodeRequest(data).then((response) => {
                if (response.status === 200) {
                    let response_amount = response.data.amount
                    if (delivering) {
                        response_amount += 450
                    }
                    setAmount(response_amount)
                    setPromoCodeState(true)
                } else if (response.status === 400) {
                    alert(JSON.parse(response.responseText));
                }
            })
        } else {
            alert('Сначала введите промокод!')
        }
    }

    return(
        <>
            <div className="popup-cart__input-email-wrapper">
                <label className="popup-cart__email-label _label">
                    Email
                    <p>
                <span style={{fontSize: "14px"}}>
                    (Для отправки чека на email)
                </span>
                    </p>
                </label>
                <input type="text" name='email'
                       placeholder="Требуется указать при онлайн оплате"
                       className="popup-cart__email-input _input"/>
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
                <input name='delivery_address' type="text" disabled
                       placeholder="Пример: ул. Пушкинская 4"
                       className="popup-cart__address-input _input"/>
            </div>
            <div className="popup-cart__date-wrapper">
                <label className="popup-cart__date-label _label">Дата доставки /
                    Самовывоза </label>
                <input name='delivery_date' type="date" required
                       className="popup-cart__date-input _input"/>
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
                <select name='delivery_time' defaultValue="" disabled
                        className="popup-cart__time-input _input">
                    <option disabled value="">Выберите время доставки</option>
                    <option value="10:00 - 12:00">10:00 - 12:00</option>
                    <option value="12:00 - 15:00">12:00 - 15:00</option>
                    <option value="15:00 - 18:00">15:00 - 18:00</option>
                    <option value="18:00 - 21:00">18:00 - 21:00</option>
                    <option value="21:00 - 00:00">21:00 - 00:00</option>
                </select>
            </div>
            <div className="popup-cart__checkbox-wrapper">
                <label className="popup-cart__checkbox-label">
                    <input onClick={(e) => setReceiver(e.target.closest('form'))}
                           type="checkbox" name="customer_is_receiver"
                           className="popup-cart__checkbox-input"/>
                    Заказчик является получателем заказа
                </label>
            </div>
            <div className="popup-cart__input-name-wrapper">
                <label className="popup-cart__name-label _label">Имя
                    получателя</label>
                <input type="text" className="popup-cart__name-input _input"
                       name="receiver_name" placeholder="Введите имя получателя"
                       required maxLength="50" minLength="2"/>
            </div>
            <div className="popup-cart__input-phone-wrapper">
                <label className="popup-cart__phone-label _label">Телефон
                    получателя</label>
                <input type="text" onClick={(e) => formatPhoneNumber(e)}
                       placeholder="Например: +7 (999) 777-77-77"
                       className="popup-cart__phone-input _input"
                       name="receiver_phone_number" required
                       maxLength="20" minLength="11"/>
            </div>
            <div className="popup-cart__checkbox-wrapper">
                <label className="popup-cart__checkbox-label">
                    <input onClick={(e) => changeDeliveringPrice(e)} type='checkbox'
                           name="delivering" className="popup-cart__checkbox-input"/>
                    С доставкой (+450 рублей)
                </label>
            </div>
            <div className="popup-cart__checkbox-wrapper">
                <label className="popup-cart__checkbox-label">
                    <input type='checkbox' name='cash'
                           className="popup-cart__checkbox-input"/>
                    Оплатить наличными при получении
                </label>
            </div>
            <div className="popup-cart__checkbox-wrapper">
                <label className="popup-cart__checkbox-label">
                    <input type='checkbox' name='without_calling'
                           className="popup-cart__checkbox-input"/>
                    <span> Напишите мне в whatsapp/telegram (Не звонить) </span>
                </label>
            </div>
            <div className="popup-cart__input-name-wrapper">
                <label className="popup-cart__name-label _label">Примечание</label>
                <textarea className="textarea_note"
                          placeholder="Напишите примечание, если оно требуется"
                          name="note" maxLength="300"></textarea>
            </div>
            <div className="popup-cart__input-name-wrapper">
                <label className="popup-cart__name-label _label">Промокод</label>
                <input type="text" className="popup-cart__name-input _input"
                       name="promo_code" placeholder="Промокод (при наличии)"
                       maxLength="25"/>
            </div>
            <div className="popup-cart__set-promo_code-button-wrapper">
                <button onClick={(e) => setPromoCode(e)}
                        className="popup-cart__set-promo_code-button _black-button-promo-code">Применить
                    промокод
                </button>
            </div>
            <div className="popup-cart__product-price">Сумма без учёта
                доставки: {amount - delivering} ₽
            </div>
            <div className="popup-cart__delivery-price">Доставка: {delivering} ₽
            </div>
            <div className="popup-cart__last-price">Итоговая сумма: {amount} ₽</div>
            <div className="popup-cart__create-order-button-wrapper">
                <button onClick={(e) => createPayment(e)}
                        className="popup-cart__create-order-button _black-button">Оформить
                    заказ
                </button>
            </div>
            <div className="popup-cart__time-label _label" style={{marginTop: "30px"}}>
                Нажимая на кнопку "Оформить заказ" вы автоматически соглашаетесь
                <Link to={`/privacy_policy`}>
                    <span> на обработку персональных данных и с политикой конфиденциальности </span>
                </Link>
            </div>
        </>
    );
}

export default FullPaymentForm;
