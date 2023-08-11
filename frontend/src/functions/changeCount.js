import changeAmount from './changeAmount';


const changeCount = (event, setAmount) => {
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
            const result = changeAmount(target);
            if (result === false) {
                --value;
            } else {
                setAmount(result)
            }
        }

        if (value < 1) {
            target.closest('.popup-item-cart__count-block').querySelector('.popup-item-cart__plus-button').classList.add('disabled');
        } else {
            target.closest('.popup-item-cart__count-block').querySelector('.popup-item-cart__minus-button').classList.remove('disabled');
        }

    return value;

    }
}

export default changeCount;
