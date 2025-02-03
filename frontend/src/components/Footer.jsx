import {Link} from 'react-router-dom';


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
                                    <Link className="item-footer__sub-link">Принимаем заказы по:</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="https://wa.me/79934461702" className="item-footer__sub-link">WhatsApp: +7 (993) 446-17-02</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link className="item-footer__sub-link">Email: crocusrnd@mail.ru</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="tel: +7 (993) 446-17-02" className="item-footer__sub-link">Звонок: +7 (993) 446-17-02</Link>
                                </li>
                            </ul>
                        </li>
                        <li className="footer__item item-footer">
                            <Link className="item-footer__link">
                                Социальные сети
                            </Link>
                            <ul className="item-footer__sub-list">
                                <li className="item-footer__sub-item">
                                    <Link to="https://instagram.com/crocusrnd/" className="item-footer__sub-link">Instagram</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="https://wa.me/79934461702" className="item-footer__sub-link">Whatsapp</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="https://t.me/crocus_rnd/" className="item-footer__sub-link">Telegram</Link>
                                </li>
                            </ul>
                        </li>
                        <li className="footer__item item-footer">
                            <Link className="item-footer__link">
                                Связь с нами
                            </Link>
                            <ul className="item-footer__sub-list">
                                <li className="item-footer__sub-item">
                                    <Link to="https://wa.me/79934461702/" className="item-footer__sub-link">Whatsapp: +7 (993) 446-17-02</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="https://instagram.com/crocusrnd/" className="item-footer__sub-link">Instagram: @crocusrnd</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link className="item-footer__sub-link">Email: crocusrnd@mail.ru</Link>
                                </li>
                                <li className="item-footer__sub-item">
                                    <Link to="https://t.me/crocus_rnd/" className="item-footer__sub-link">Telegram: @crocus_rnd</Link>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
                <div className="footer__content">
                    <div className="footer__content-container _container">
                        <p className="footer__copy">© <span> {new Date().getFullYear()} </span> CROCUS RND - ЦВЕТЫ РОСТОВ-НА-ДОНУ</p>
                        <ul className="footer__socials-list footer-socials">
                            <li className="footer-socials__item">
                                <Link to="https://wa.me/79934461702" className="footer-socials__link">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                                        <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                                    </svg>
                                </Link>
                            </li>
                            <li className="footer-socials__item">
                                <Link to="https://t.me/crocus_rnd/" className="footer-socials__link">
                                    <svg width="24px" height="24px" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" xmlSpace="preserve" xmlnsserif="http://www.serif.com/" >
                                        <path id="telegram-5" d="M12,0c-6.627,0 -12,5.373 -12,12c0,6.627 5.373,12 12,12c6.627,0 12,-5.373 12,-12c0,-6.627 -5.373,-12 -12,-12Zm0,2c5.514,0 10,4.486 10,10c0,5.514 -4.486,10 -10,10c-5.514,0 -10,-4.486 -10,-10c0,-5.514 4.486,-10 10,-10Zm2.692,14.889c0.161,0.115 0.368,0.143 0.553,0.073c0.185,-0.07 0.322,-0.228 0.362,-0.42c0.435,-2.042 1.489,-7.211 1.884,-9.068c0.03,-0.14 -0.019,-0.285 -0.129,-0.379c-0.11,-0.093 -0.263,-0.12 -0.399,-0.07c-2.096,0.776 -8.553,3.198 -11.192,4.175c-0.168,0.062 -0.277,0.223 -0.271,0.4c0.006,0.177 0.125,0.33 0.296,0.381c1.184,0.354 2.738,0.847 2.738,0.847c0,0 0.725,2.193 1.104,3.308c0.047,0.139 0.157,0.25 0.301,0.287c0.145,0.038 0.298,-0.001 0.406,-0.103c0.608,-0.574 1.548,-1.461 1.548,-1.461c0,0 1.786,1.309 2.799,2.03Zm-5.505,-4.338l0.84,2.769l0.186,-1.754c0,0 3.243,-2.925 5.092,-4.593c0.055,-0.048 0.062,-0.13 0.017,-0.188c-0.045,-0.057 -0.126,-0.071 -0.188,-0.032c-2.143,1.368 -5.947,3.798 -5.947,3.798Z"/>
                                    </svg>
                                </Link>
                            </li>
                            <li className="footer-socials__item">
                                <Link to="https://instagram.com/crocusrnd/" className="footer-socials__link">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                                        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                                    </svg>
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </footer>
    )
}

export default Footer;
