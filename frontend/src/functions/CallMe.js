import CallMeRequest from '../API/CallMeRequest';


const CallMe = async (event) => {
    event.preventDefault();


    const form = event.target.closest('form');
    const isMobilePhone = (str) => /^\+?[7, 8]\s*\(?\d{3}\)?\s*\d{3}-?\d{2}-?\d{2}$/.test(str);
    if (isMobilePhone(form.phone_number.value) === false) {
        alert('Телефон не соответствует СНГ формату, убедитесь в том, что номер написан верно');
        return null;
    }

    await CallMeRequest(form.phone_number.value).then((response) => {
        if (response.status === 200) {
            alert(response.data)
        } else if (response.status === 400) {
            alert(JSON.parse(response.responseText))
        } else if (response.status === 403) {
            alert(JSON.parse(response.responseText))
        } else if (response.status === 500) {
            alert('Произошла ошибка на стороне сервера, попробуйте обновить страничку и повторить заказ снова')
        }
    })

}

export default CallMe;
