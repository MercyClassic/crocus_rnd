import Header from '../components/Header';
import Footer from '../components/Footer';
import {Link} from 'react-router-dom';


const ContactInformation = () => {
    return(
        <>
        <Header />
            <main className="main">
                <section className="creator-letter">
                    <div className="creator-letter__container">
                        <h3 style={{fontSize: "30px"}} className="creator-letter__title _title">КОНТАКТНАЯ ИНФОРМАЦИЯ</h3>
                        <div style={{textAlign: "center", fontSize: "26px", lineHeight: "1.5"}} className="creator-letter__body _letter">
                            <ul className="item-footer__sub-list">
                                <li className="menu__sub-item">
                                    <Link to="https://wa.me/79185212571/" className="catalog__link">Whatsapp: +7 (993) 446-17-02</Link>
                                </li>
                                <li className="menu__sub-item">
                                    <Link to="tel: +7 (918) 521-25-71" className="catalog__link">Звонок: +7 (993) 446-17-02</Link>
                                </li>
                                <li className="menu__sub-item">
                                    <Link to="https://instagram.com/crocusrnd/" className="catalog__link">Instagram: @crocusrnd</Link>
                                </li>
                                <li className="menu__sub-item">
                                    <Link className="catalog__link">Email: crocusrnd@mail.ru</Link>
                                </li>
                                <li className="menu__sub-item">
                                    <Link className="catalog__link">
                                        <p> ИП Сабанова Елена Александровна </p>
                                        <p> ОГРНИП 318619600091608 </p>
                                        <p> ИНН 612890171437 </p>
                                    </Link>
                                </li>
                            </ul>
                        </div>
                    </div>
                </section>
            </main>
            <Footer/>
        </>
    );
}

export default ContactInformation;
