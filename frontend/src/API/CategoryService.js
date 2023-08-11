import axios from 'axios';


export default class PostService {
    static async getCategories() {
        const response = await axios.get(`/api/v1/categories`)
        return response.data
    }
}
