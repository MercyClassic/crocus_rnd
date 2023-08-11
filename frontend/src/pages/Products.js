import React, {useState, useEffect, useContext} from 'react';
import {useLocation} from 'react-router-dom'
import ProductService from '../API/ProductService';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ProductList from '../components/ProductList';
import Catalog from '../components/Catalog';
import Search from '../components/Search';
import Delivery from '../components/Delivery';
import Cart from '../components/Cart';
import Loader from '../components/Loader';
import useFetching from '../hooks/useFetching';
import {CountCartProductsContext} from '../context';


function Products({favourites=false}) {
    const {countCartProducts, setCountCartProducts} = useContext(CountCartProductsContext);

    const [productsData, setProducts] = useState([]);
    const location = useLocation();
    const [fetchProducts, isProductsLoading, productsError] = useFetching(async () => {
        let products = [];
        if (favourites) {
            products = await ProductService.getFavourites(location.search);
        } else {
            products = await ProductService.getProducts(location.search);
        }
        setProducts(products);
    });

    useEffect(() => {
        fetchProducts();
    }, [location.search, location.pathname])

    useEffect(() => {
        if (productsData.cart_products) {
            setCountCartProducts(productsData.cart_products.length);
        }
    }, [productsData.cart_products])

    return (
        <>
            <Header/>
            <main className="main">
                <Cart requestCountCartProducts={productsData.cart_products && productsData.cart_products.length} />
                <Catalog />
                <Search />
                <Delivery />
                {productsError.status === 500 &&
                    alert('Неизвестная ошибка на стороне сервера, приносим свои извинения')
                }
                {isProductsLoading
                    ? <Loader />
                    : <ProductList data={productsData} />
                }
            </main>
            <Footer/>
        </>
    );
}

export default Products;
