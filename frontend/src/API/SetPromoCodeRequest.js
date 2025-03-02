import axios from 'axios';


const SetPromoCodeRequest = async (data) => {
    try {
        const response = await axios.post(
            `/api/v1/get_promo_code_discount`,
            {...data}
        )
        return response
    } catch (e) {
        return e.request
    }
}

export default SetPromoCodeRequest;
