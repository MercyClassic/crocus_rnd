import {Link} from 'react-router-dom';
import maxIcon from "../static/img/svg/max.svg";
import vkIcon from "../static/img/svg/vk.svg";


const Footer = () => {
    return (
        <footer className="footer">
                <div className="footer__container _container">
                    <ul className="footer__list">
                        <li className="footer__item item-footer">
                            <Link className="item-footer__link">
                                КОНТАКТНАЯ ИНФОРМАЦИЯ
                            </Link>
                            <ul className="item-footer__sub-list">
                                <li className="item-footer__sub-item">
                                    <Link className="item-footer__sub-link">Принимаем
                                        заказы по:</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="tel: +7 (993) 446-17-02"
                                          className="item-footer__sub-link">Мессенджеры:
                                        +7 (993) 446-17-02</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="tel: +7 (993) 446-17-02"
                                          className="item-footer__sub-link">Звонок:
                                        +7 (993) 446-17-02</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link className="item-footer__sub-link">Email:
                                        crocusrnd@mail.ru</Link>
                                </li>
                            </ul>
                        </li>
                        <li className="footer__item item-footer">
                            <Link className="item-footer__link">
                                Связь с нами
                            </Link>
                            <ul className="item-footer__sub-list">
                                <li className="item-footer__sub-item">
                                    <Link className="item-footer__sub-link">Мессенджеры:
                                        +7 (993) 446-17-02</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link
                                        to="https://max.ru/u/f9LHodD0cOJK18O_kYrguhCsb1GtmdmcN6afC1jJSJYZSQ2DsV9JLOcpFBI"
                                        className="item-footer__sub-link">Max: +7
                                        (993) 446-17-02</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link
                                        to="https://vk.com/elenflowersrostov"
                                        className="item-footer__sub-link">VK: ELEN
                                        FLOWERS</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link className="item-footer__sub-link">Email:
                                        crocusrnd@mail.ru</Link>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            <div className="footer__content">
                <div className="footer__content-container _container">
                    <p className="footer__copy">© <span> {new Date().getFullYear()} </span> КРОКУС
                        РНД - ЦВЕТЫ РОСТОВ-НА-ДОНУ</p>
                    <ul className="footer__socials-list footer-socials">
                        <li className="footer-socials__item">
                            <Link
                                to="https://max.ru/u/f9LHodD0cOJK18O_kYrguhCsb1GtmdmcN6afC1jJSJYZSQ2DsV9JLOcpFBI"
                                className="footer-socials__link">
                                <img src={maxIcon} alt="Max"/>
                            </Link>
                        </li>
                        <li className="footer-socials__item">
                            <Link
                                to="https://vk.com/elenflowersrostov"
                                className="footer-socials__link">
                                <img src={vkIcon} alt="Max"/>
                            </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </footer>
    )
}

export default Footer;
