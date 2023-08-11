const setReceiver = (form) => {
    const customer_name = form.customer_name;
    const customer_phone_number = form.customer_phone_number;
    const receiver_name = form.receiver_name;
    const receiver_phone_number = form.receiver_phone_number;
    if (form.customer_is_receiver.checked) {
        receiver_name.value = customer_name.value;
        receiver_phone_number.value = customer_phone_number.value;
        receiver_name.setAttribute('disabled', true)
        receiver_phone_number.setAttribute('disabled', true)
    } else {
        receiver_name.removeAttribute('disabled')
        receiver_phone_number.removeAttribute('disabled')
    }
}

export default setReceiver;
