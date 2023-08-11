import {Link} from 'react-router-dom';
import { useState, useContext } from 'react';
import ProductService from '../API/ProductService';
import useFetching from '../hooks/useFetching';
import Loader from './Loader';
import FullPaymentForm from './FullPaymentForm';
import changeCount from '../functions/changeCount';
import formatPhoneNumber from '../functions/formatPhoneNumber';
import deleteFromCart from '../functions/deleteFromCart';
import {CountCartProductsContext} from '../context';


const CartItem = ({product, setAmount}) => {
    const [count, setCountState] = useState(1);

    const setCount = async (event) => {
        let value = changeCount(event, setAmount);
        if (value === 0) {
            await deleteFromCart(event.target);
            value = 1;
        }
        setCountState(value);
    }

    return(
        <li className="popup-cart__item popup-item-cart">
            <div className="popup-item-cart__image-wrapper">
                <img src={product.image} alt="product"/>
            </div>
            <h6 className="popup-item-cart__title"><Link to={product.url}> {product.title} </Link></h6>
            <div name="price" data-price={product.price} >{product.price}₽</div>
            <div onClick={(e) => setCount(e)} className="popup-item-cart__count-block" data-counter>
                <div className="popup-item-cart__minus-button" data-action='minus'>
                    <span></span>
                </div>
                <input className="popup-item-cart__input" type="text" value={count} disabled data-slug={product.slug}/>
                <div className="popup-item-cart__plus-button" data-action='plus'>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </li>
    );
}


export const CartModal = ({cartProducts=[], visible, setVisible}) => {
    const [preContinueForm, setContinueForm] = useState(false);
    const [amount, setAmount] = useState(cartProducts.reduce((sum, product) => sum + product.price, 0));

    let rootClasses = ['cart']
    if (!visible) {
        rootClasses.push('non_visible');
    }

    const showFullPaymentCreate = (event) => {
        setContinueForm(true);
    }

    return(
        <section className={rootClasses.join(' ')} onClick={() => setVisible(false)}>
            <div className="cart__popup popup-cart">
                <div className="popup-cart__wrapper" onClick={(e) => e.stopPropagation()}>
                    <div className="popup-cart__header-wrapper">
                        <h5 className="popup-cart__title">Ваш заказ:</h5>
                            <button className="popup-cart__close-button" onClick={() => setVisible(false)}>
                                <span></span>
                                <span></span>
                            </button>
                    </div>
                    <form className="popup-cart__form" method="POST">
                        <ul className="popup-cart__product-list">
                            {!cartProducts.length
                                ? <div> Корзина пуста </div>
                                : <>
                                    {cartProducts.map((product) =>
                                        <CartItem product={product} setAmount={setAmount} key={product.id} />
                                    )}
                                  </>
                            }
                        </ul>
                        <div className="popup-cart__price" data-amount={amount}>Сумма: {amount} ₽</div>
                        <div className="popup-cart__input-name-wrapper">
                            <label className="popup-cart__name-label _label">Ваше имя</label>
                            <input type="text" className="popup-cart__name-input _input" name="customer_name" placeholder="Введите ваше имя" required maxLength="150" minLength="2" />
                        </div>
                        <div className="popup-cart__input-phone-wrapper">
                            <label className="popup-cart__phone-label _label">Ваш телефон</label>
                            <input onClick={(e) => formatPhoneNumber(e)} type="text" placeholder="Например: +7 (999) 777 77 77" className="popup-cart__phone-input _input" name="customer_phone_number" required maxLength="20" minLength="11" />
                        </div>
                        <div className="popup-cart__next-button-wrapper">
                            <button onClick={(e) => showFullPaymentCreate(e)} type="button" className="popup-cart__next-button _black-button">Продолжить</button>
                        </div>

                        {preContinueForm && <FullPaymentForm form={document.querySelector('.popup-cart__form')} amount={amount} setAmount={setAmount} />}

                    </form>
                </div>
            </div>
            <div className="overlay"></div>
        </section>
    );
}

const Cart = () => {
    const {countCartProducts, setCountCartProducts} = useContext(CountCartProductsContext);

    const [cart, setCartVisible] = useState(false);
    const [cartProducts, setCartProducts] = useState([]);
    const [fetchCart, isLoading, cartError] = useFetching(async() => {
        const data = await ProductService.getCart();
        setCartProducts(data);
        setCartVisible(true);
    })

    return(
        <>
        <div className="cart__icon icon-cart">
            <Link onClick={() => fetchCart()} href="/api/v1/cart/" className="icon-cart__wrapper">
                <div className="icon-cart__body">
                    <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                       <path d="M23.52,29h-15a5.48,5.48,0,0,1-5.31-6.83L6.25,9.76a1,1,0,0,1,1-.76H24a1,1,0,0,1,1,.7l3.78,12.16a5.49,5.49,0,0,1-.83,4.91A5.41,5.41,0,0,1,23.52,29ZM8,11,5.11,22.65A3.5,3.5,0,0,0,8.48,27h15a3.44,3.44,0,0,0,2.79-1.42,3.5,3.5,0,0,0,.53-3.13L23.28,11Z"/>
                        <path d="M20,17a1,1,0,0,1-1-1V8a3,3,0,0,0-6,0v8a1,1,0,0,1-2,0V8A5,5,0,0,1,21,8v8A1,1,0,0,1,20,17Z"/>
                    </svg>
                </div>
                    <div className="icon-cart__count">{countCartProducts}</div>
            </Link>
        </div>
        {cartError.status === 500 &&
            alert('Неизвестная ошибка на стороне сервера, приносим свои извинения')
        }
        {isLoading
            ? <Loader />
            : <CartModal cartProducts={cartProducts} visible={cart} setVisible={setCartVisible} />
        }
        </>
    );
}

export default Cart;
