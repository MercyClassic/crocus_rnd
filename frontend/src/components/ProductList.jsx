import { useEffect } from 'react';
import { useLocation, Link, useSearchParams } from 'react-router-dom';
import Product from './Product';


const ProductList = ({data}) => {
    const location = useLocation();
    const [searchParams, setSearchParams] = useSearchParams();
    const products = data.result;
    const cart_products = data.cart_products;
    const favourites = data.favourites;

    const onLoad = () => {
        if (location.search.includes('&catalog')) {
            let url = window.location.href.replace('&catalog', '');
            searchParams.delete('catalog')
            setSearchParams(searchParams)
            document.getElementById('catalog').scrollIntoView({behavior: 'smooth'});
        }
    }

    useEffect(() => {
        onLoad();
    }, [location.search])

    return(
        <section className="flower">
            <div className="flower__container _container">
                <div className="flower__heading _heading">
                    <h2 id="catalog" className="flower__title _title">АКТУАЛЬНОЕ ПРЕДЛОЖЕНИЕ</h2>
                </div>
                {products === undefined || !products.length
                    ? <div style={{fontSize: "30px", lineHeight: "1.5"}}>
                          <h1> Ничего не найдено </h1>
                          <Link to="/"> Вернуться на главную страницу </Link>
                      </div>
                    : <ul className="flower__list">
                        {products.map((product) =>
                            <Product product={product} cart_products={cart_products} favourites={favourites} key={product.id} />
                        )}
                       </ul>
                }
            </div>
        </section>
    );
}

export default ProductList;
