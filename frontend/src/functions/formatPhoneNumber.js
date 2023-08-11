const formatPhoneNumber = (event) => {
    if (event.target.value === '') {
        event.target.value = '+7';
    }
}

export default formatPhoneNumber;
