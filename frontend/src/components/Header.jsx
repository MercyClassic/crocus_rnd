import {Link} from 'react-router-dom';
import {isMobile} from 'react-device-detect';


const Header = () => {

    const documentActions = (e) => {
        const targetElement = e.target;
        if (window.innerWidth > 1200 && isMobile) {
            if (targetElement.classList.contains('menu__link')) {
                targetElement.closest('.menu__item').classList.toggle('_hover');
            }
        }
        if (targetElement.classList.contains('icon-menu')) {
            document.querySelector('.wrapper').classList.toggle('_active');
            document.querySelector('.icon-menu').classList.toggle('_active');
            document.querySelector('.menu').classList.toggle('_active');
            document.querySelector('.actions__tel').classList.toggle('_active');
        }
    }

    return (
        <header onClick={(e) => documentActions(e)} className="header">
            <div className="header__container">
                <div className="header__body">
                    <div className="header__menu menu ">
                        <nav className="menu__body">
                            <ul className=" menu__list">
                                <li className="menu__item">
                                    <div className="menu__link-wrapper">
                                        <Link to="/" className="menu__link menu__link-arrow">Каталог цветов</Link>
                                        <button type="button" className="menu__arrow">
                                            <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <path
                                                    d="M8.75 3.70096C9.75 4.27831 9.75 5.72169 8.75 6.29904L2.75 9.76314C1.75 10.3405 0.5 9.6188 0.5 8.4641L0.500001 1.5359C0.500001 0.381198 1.75 -0.34049 2.75 0.23686L8.75 3.70096Z"
                                                    fill="#2B303B" />
                                            </svg>
                                        </button>
                                        <ul className="menu__sub-list">
                                            <li className="menu__sub-item">
                                                <Link to="/" className="menu__sub-link">Все</Link>
                                            </li>
                                            <li className="menu__sub-item">
                                                <Link to="?type=bouquet" className="menu__sub-link">Букеты</Link>
                                            </li>
                                            <li className="menu__sub-item">
                                                <Link to="?type=box" className="menu__sub-link">Коробки</Link>
                                            </li>
                                            <li className="menu__sub-item">
                                                <Link to="?type=basket" className="menu__sub-link">Корзинки</Link>
                                            </li>
                                        </ul>
                                    </div>
                                </li>

                                <li className="menu__item">
                                    <div className="menu__link-wrapper">
                                        <Link className="menu__link menu__link-arrow">Магазин</Link>
                                        <ul className="menu__sub-list">
                                            <li className="menu__sub-item">
                                                <Link to="/about_shop" className="menu__sub-link">О нас</Link>
                                            </li>
                                            <li className="menu__sub-item">
                                                <Link to="/contact_information" className="menu__sub-link">Контактная информация</Link>
                                            </li>
                                            <li className="menu__sub-item">
                                                <Link to="/privacy_policy" className="menu__sub-link">Политика конфиденциальности</Link>
                                            </li>
                                        </ul>
                                    </div>
                                    <button type="button" className="menu__arrow">
                                        <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path
                                                d="M8.75 3.70096C9.75 4.27831 9.75 5.72169 8.75 6.29904L2.75 9.76314C1.75 10.3405 0.5 9.6188 0.5 8.4641L0.500001 1.5359C0.500001 0.381198 1.75 -0.34049 2.75 0.23686L8.75 3.70096Z"
                                                fill="#2B303B" />
                                        </svg>
                                    </button>
                                </li>
                                <li className="menu__item">
                                    <Link to="/favourites" className="menu__link">Избранное</Link>
                                </li>
                            </ul>
                        </nav>
                    </div>
                    <Link to="/" className="header__logo">
                        <img src={require("../static/img/png/logo.png")} alt="Logo" className="header__logo"/>
                    </Link>
                    <div className="header__actions actions">
                        <div className="actions__contact">
                            <Link to="https://wa.me/79185212571" className="actions__whatsapp-icon">
                                <img src={require("../static/img/png/whatsapp.png")} alt="Whatsapp"/>
                            </Link>
                            <Link to="https://wa.me/79185212571" className="actions__tel ">+7 (918) 521-25-71</Link>
                            <Link to="https://wa.me/79185212571" className="actions__whatsapp-text">Написать в Whatsapp</Link>
                            <Link className="icon-menu">
                                <span></span>
                                <span></span>
                                <span></span>
                            </Link>
                        </div>
                        <Link to="https://wa.me/79185212571" className="actions__fast-call">Перейти в Whatsapp</Link>
                    </div>
                </div>
            </div>
        </header>
    )
}

export default Header;