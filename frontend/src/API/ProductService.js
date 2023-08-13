import axios from 'axios';


const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

axios.defaults.withCredentials = true
axios.defaults.headers.post['X-CSRFToken'] = getCookie('csrftoken');


export default class PostService {
    static async getProducts(search) {
        const response = await axios.get(`/api/v1/flowers${search}`)
        return response.data
    }

    static async getProduct(slug) {
        const response = await axios.get(`/api/v1/flowers/${slug}`)
        return response.data
    }

    static async getCart() {
        const response = await axios.get(`/api/v1/cart`)
        return response.data
    }

    static async addToSession(slug, type) {
        const response = await axios.post(
            `/api/v1/add_to_session/${slug}`,
            {type: type},
        )
        return response.status
    }

    static async getFavourites(search) {
        const response = await axios.get(`/api/v1/favourites${search}`)
        return response.data
    }
}
