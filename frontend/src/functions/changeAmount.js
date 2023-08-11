const changeAmount = (target) => {
    const form = target.closest('form')
    const amount = form.querySelector('.popup-cart__price');
    const price = Number(target.closest('li').children.price.dataset.price);
    let result = 0;
    if (target.dataset.action === 'plus') {
        result = Number(amount.dataset.amount) + price;
    } else if (target.dataset.action === 'minus') {
        result = Number(amount.dataset.amount) - price;
    }

    if (result > 50000) {
        alert('Для заказа свыше 50 000 рублей, свяжитесь с продавцом');
        return false;
    }
    return result;
}

export default changeAmount;
