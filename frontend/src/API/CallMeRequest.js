import axios from 'axios';


const CallMeRequest = async(phone_number) => {
    try {
        const response = await axios.post(
            `/api/v1/call_me`,
            {phone_number: phone_number},
        )
        return response;
    } catch (e) {
        return e.request;
    }
};

export default CallMeRequest;
