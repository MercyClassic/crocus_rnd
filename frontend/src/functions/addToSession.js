import ProductService from '../API/ProductService';
import InCartSvg from '../components/Svg/InCart';
import NotInCartSvg from '../components/Svg/NotInCart';
import RedHeartSvg from '../components/Svg/RedHeart';
import BlackHeartSvg from '../components/Svg/BlackHeart';


const getListButton = (status, type) => {
    if (status === 201) {
        if (type === 'favourite') {
             return <RedHeartSvg />
        } else {
             return <InCartSvg />
        }
    } else if (status === 204) {
        if (type === 'favourite') {
             return <BlackHeartSvg />
        } else {
             return <NotInCartSvg />
        }
    }
}

const getDetailButton = (status, type) => {
    if (status === 201) {
        if (type === 'favourite') {
             return <RedHeartSvg />
        } else {
             return <button className="product-content__delete-button">Удалить из корзины</button>
        }
    } else if (status === 204) {
        if (type === 'favourite') {
             return <BlackHeartSvg />
        } else {
             return <button className="product-content__add-button">Добавить в корзину</button>
        }
    }
}

const addToSession = async (event, detail=false) => {
    event.preventDefault();
    const form = event.target.closest('form');
    const type = form.dataset.type;
    const slug = form.dataset.slug;
    const button = await ProductService.addToSession(slug, type)
    .then((status) => {
        if (detail) {
            return getDetailButton(status, type)
        } else {
            return {status, button: getListButton(status, type)}
        }
    });
    return button;
}

export default addToSession;
