import axios from 'axios';


const PaymentCreateRequest = async (data) => {
    try {
        const response = await axios.post(
            `/api/v1/create_payment`,
            {...data}
        )
        return response
    } catch (e) {
        return e.request
    }
}

export default PaymentCreateRequest;
