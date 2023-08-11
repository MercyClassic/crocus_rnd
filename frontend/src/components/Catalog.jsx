import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import useFetching from '../hooks/useFetching';
import CategoryService from '../API/CategoryService';


const Category = ({category}) => {
    return(
        <li className="catalog__item">
            <Link to={`?category=${category.name}&catalog`} className="catalog__link">
                <div className="catalog__image">
                    <img src={category.image} alt="category"/>
                </div>
                <p className="catalog__title">{category.name}</p>
            </Link>
        </li>
    );
}

const CatalogImplement = ({categories}) => {
    if (!categories) {
        return null;
    }

    return(
        <section className="catalog">
            <div className="catalog__container">
                <div className="catalog__body" >
                    <ul className="catalog__list">
                        {categories.map((category) =>
                            <Category category={category} key={category.id} />
                        )}
                    </ul>
                </div>
            </div>
        </section>
    );
}

const Catalog = () => {
    const [categories, setCategories] = useState([]);
    const [fetchCategories, isLoading, categoryError] = useFetching(async () => {
        const data = await CategoryService.getCategories();
        setCategories(data);
    })


    useEffect(() => {
        fetchCategories();
    }, [])

    return(
        <CatalogImplement categories={categories} />
    );
}

export default Catalog;
