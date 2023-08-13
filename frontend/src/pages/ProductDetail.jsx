import {useState, useEffect} from 'react';
import {Link, useParams} from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import useFetching from '../hooks/useFetching';
import ProductService from '../API/ProductService';
import Loader from '../components/Loader';
import { CartModal } from '../components/Cart';
import RedHeartSvg from '../components/Svg/RedHeart';
import BlackHeartSvg from '../components/Svg/BlackHeart';
import addToSession from '../functions/addToSession';


function ProductExtraImage({image, changeMainPicture}) {
    return(
        <button onClick={(e) => changeMainPicture(e)} className="main-product__slider-image-wrapper">
            <img src={image.image} alt="Slider" />
        </button>
    );
}

function getLikeButton(slug, favourites) {
    if (favourites.includes(slug)) {
        return(
            <RedHeartSvg />
        );
    } else {
        return(
            <BlackHeartSvg />
        );
    }

}

function getKindLink(kind) {
    if (kind) {
        return(
            <Link to="/?type={kind}" className="product-info__category-button">{kind}</Link>
        )
    } else {
    return(
            <Link to="/" className="product-info__category-button">Все категории</Link>
        )
    }
}

function getAddToCartButton(slug, cart_products) {
    if (cart_products.includes(slug)) {
        return(
            <button className="product-content__delete-button">Удалить из корзины</button>
        )
    } else {
    return(
            <button className="product-content__add-button">Добавить в корзину</button>
        )
    }
}

const ProductDetailPage = ({data, setCartVisible}) => {
    const product = data.result;
    const cartProducts = data.cart_products;
    const favourites = data.favourites;

    const [mainPicture, setMainPicture] = useState(product && product.image);
    const [cartButton, setCartButton] = useState(null);
    const [likeButton, setLikeButton] = useState(null);

    const changeButton = async (event) => {
        const button = await addToSession(event, true);
        const type = event.target.closest('form').dataset.type
        if (type === 'cart') {
            setCartButton(button);
        } else if (type === 'favourite') {
            setLikeButton(button);
        }
    }

    const changeMainPicture = (event) => {
        setMainPicture(event.target.getAttribute('src'));
    }

    if (product) {
        return(
            <>
                <section className="product">
                    <div className="product__container _container">
                        <div className="product__header header-product">
                        </div>
                        <div className="product__main main-product">
                            <div className="main-product__slider-wrapper">
                                <div className="main-product__image-wrapper">
                                    <img src={mainPicture} alt="Product" />
                                </div>
                                <ul className="main-product__sliders">
                                    <button onClick={(e) => changeMainPicture(e)} className="main-product__slider-image-wrapper">
                                        <img src={product.image} alt="Slider" />
                                    </button>
                                        {product.images &&
                                            product.images.map((image) =>
                                                <ProductExtraImage changeMainPicture={changeMainPicture} image={image} key={image.id} />
                                            )
                                        }
                                </ul>
                            </div>
                            <div className="main-product__content product-content">
                                <h2 className="product-content__title" data-slug={product.slug}>{product.title}</h2>
                                <div className="product-content__article">АРТИКУЛ: {product.id}</div>
                                <div className="product-content__price-wrapper">
                                    <p className="product-content__price" data-price={product.price}>{product.price}₽</p>
                                    <form onClick={(e) => changeButton(e)} method="post" className="card-pion__favourites" data-type="favourite" data-slug={product.slug}>
                                        <button name="action-button">
                                            {!likeButton
                                                ? getLikeButton(product.slug, favourites)
                                                : likeButton
                                            }
                                        </button>
                                    </form>
                                </div>
                                <div className="product-content__buy-block">
                                    <form onClick={(e) => changeButton(e)} method="post" data-type="cart" data-slug={product.slug}>
                                        {!cartButton
                                            ? getAddToCartButton(product.slug, cartProducts)
                                            : cartButton
                                        }
                                    </form>
                                        <button onClick={() => setCartVisible(true)} className="product-content__buy-button">Заказ в 1 клик</button>
                                </div>
                                <div className="product-content__info product-info">
                                    <p className="product-info__sizes">Доставим быстро в <span> Любую точку Ростова</span></p>
                                    <p className="product-info__structure"> <span style={{display: "block", fontSize: "18px"}}> Описание: </span> {product.description}</p>
                                        {getKindLink(product.kind)}
                                    <p className="product-info__tip">
                                        Для заказа товара нажмите добавить в корзину или <Link to="https://wa.me/79185212571/">свяжитесь с нами</Link>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <section className="value">
                    <div className="value__container _container">
                        <ul className="value__list">
                            <li className="value__item">
                                <img src={require("../static/img/png/delivery.png")} alt="delivery" />
                                Быстрая доставка
                            </li>
                            <li className="value__item">
                                <img src={require("../static/img/png/whatsappBlack.png")} alt="delivery" />
                                Свежее фото в Whatsapp
                            </li>
                            <li className="value__item">
                                <img style={{width: "50px", height: "50px"}} src={require("../static/img/png/quality.png")} alt="delivery" />
                                Гарантия качества
                            </li>
                            <li className="value__item">
                                <img style={{width: "50px", height: "50px"}} src={require("../static/img/png/paymentOptions.png")} alt="delivery" />
                                 &nbsp; &nbsp; Множество вариантов оплаты
                            </li>
                        </ul>
                    </div>
                </section>
            </>
        );
    }
}

const ProductDetail = () => {
    const params = useParams();

    const [cart, setCartVisible] = useState(false);

    const [productData, setProduct] = useState({});
    const [fetchProduct, isLoading, ProductError] = useFetching(async () => {
        const data = await ProductService.getProduct(params.slug);
        setProduct(data);
    });

    useEffect(() => {
        fetchProduct(params.slug);
    }, []);

    return(
        <>
        <Header />
        <main className="main">
            {ProductError.length && alert(ProductError)}
            {isLoading
                ? <Loader />
                : <ProductDetailPage data={productData} setCartVisible={setCartVisible} />
            }
            {cart && <CartModal cartProducts={[productData.result]} visible={true} setVisible={setCartVisible} />}

        </main>
        <Footer />
        </>
    )

}


export default ProductDetail;
