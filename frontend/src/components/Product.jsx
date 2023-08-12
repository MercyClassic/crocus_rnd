import {useState, useContext} from 'react';
import {Link} from 'react-router-dom';
import addToSession from '../functions/addToSession';
import InCartSvg from './Svg/InCart';
import NotInCartSvg from './Svg/NotInCart';
import RedHeartSvg from './Svg/RedHeart';
import BlackHeartSvg from './Svg/BlackHeart';
import {CountCartProductsContext} from '../context';


const getAddToCartButton = (slug, cart_products) => {
    if (cart_products.includes(slug)) {
        return(
            <InCartSvg />
        )
    } else {
        return(
            <NotInCartSvg />
        )
    }
}

const getLikeButton = (slug, favourites) => {
    if (favourites.includes(slug)) {
        return(
            <RedHeartSvg />
        )
    } else {
        return(
            <BlackHeartSvg />
        )
    }
}

const Product = ({product, cart_products, favourites}) => {
    const {countCartProducts, setCountCartProducts} = useContext(CountCartProductsContext);
    const [cartButton, setCartButton] = useState(null);
    const [likeButton, setLikeButton] = useState(null);

    const changeButton = async (event) => {
        const button = await addToSession(event);
        const type = event.target.closest('form').dataset.type
        if (type === 'cart') {
            setCartButton(button.button);

            let count = countCartProducts;
            if (button.status === 201) {
                count++;
            } else {
                --count;
            }
            setCountCartProducts(count)

        } else if (type === 'favourite') {
            setLikeButton(button.button);
        }
    }

    return(
        <li className="flower__card card-flower">
            <Link to={`/flower/${product.slug}`} className="card-flower__link">
                <div className="card-flower__image">
                    <img src={product.image} alt="product"/>
                </div>
                <div className="card-flower__content">
                    <h4 className="card-flower__title">{product.title}</h4>
                    <p className="card-flower__price _card-hot-price">
                       {product.price} ₽
                    </p>
                    <div className="card-flower__actions">
                        <form onClick={(e) => changeButton(e)} method="post" className="card-flower__cart" data-type="cart" data-slug={product.slug}>
                            <button name="action_button">
                                {!cartButton
                                    ? getAddToCartButton(product.slug, cart_products)
                                    : cartButton
                                }
                            </button>
                        </form>
                        <form onClick={(e) => changeButton(e)} method="post" className="card-flower__favourites" data-type="favourite" data-slug={product.slug}>
                            <button name="action_button">
                                {!likeButton
                                    ? getLikeButton(product.slug, favourites)
                                    : likeButton
                                }
                            </button>
                        </form>
                    </div>
                </div>
            </Link>
        </li>
    );
}

export default Product;
