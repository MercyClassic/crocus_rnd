import Header from '../components/Header';
import Footer from '../components/Footer';


const AboutShop = () => {
    return(
        <>
        <Header/>
        <main className="main">
            <section className="creator-letter">
            <div className="creator-letter__container">
                <h3 className="creator-letter__title _title">О НАС</h3>
            </div>
            </section>
            <section className="about-us">
                <div className="about-us__container _container">
                    <div className="about-us__body">
                        <ul className="about-us__cards-list">
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/delivery_time.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    Время заказов | Cрок доставки готовых букетов
                                </h4>
                                <p className="about-us-card__info">
                                    Принимаем заказы ежедневно с 9:00 до 21:00. Готовые букеты доставим от 60 минут,
                                    индивидуальные авторские букеты в течение 2 часов с момента заказа.
                                </p>
                            </li>
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/map.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    География и время доставки
                                </h4>
                                <p className="about-us-card__info">
                                    Crocus -  это самые свежие цветы в Ростове-на-Дону, которые мы доставляем от 1 часа.
                                    Доставка букетов | 7 дней в неделю | 24 часа в сутки.
                                </p>
                            </li>
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/wallet.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    Оплата
                                </h4>
                                <p className="about-us-card__info">
                                    Удобный для вас метод оплаты онлайн - банковской картой или безналичным переводом на расчетный счет юр. лица.
                                    При самовывозе возможен расчет банковской картой или наличными.
                                </p>
                            </li>
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/flower.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    Свежие цветы
                                </h4>
                                <p className="about-us-card__info">
                                    Вручную собираем букеты только из свежих цветов высшего качества.
                                </p>
                            </li>
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/florist.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    Флорист
                                </h4>
                                <p className="about-us-card__info">
                                    Наши флористы всегда выслушают Ваши пожелания и соберут Ваш идеальный букет!
                                </p>
                            </li>
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/postcard.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    Открытка
                                </h4>
                                <p className="about-us-card__info">
                                    Дополним ваш букет красивой открыткой, в которой вы можете указать все что хотите.
                                </p>
                            </li>
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/wrapper.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    Уход
                                </h4>
                                <p className="about-us-card__info">
                                    Чтобы букет дольше оставался свежим,
                                    мы доставляем его в одноразовой вазе и прикладываем инструкцию по уходу за цветами.
                                </p>
                            </li>
                            <li className="about-us__card about-us-card">
                                <div className="about-us-card__image-wrapper">
                                    <img src={require("../static/abouts_us/care.svg").default} alt="1" />
                                </div>
                                <h4 className="about-us-card__title">
                                    Забота
                                </h4>
                                <p className="about-us-card__info">
                                    Уже более 5 лет мы дарим дарим яркие эмоции Вашим любимым, близким и родным.
                                    Нам важно, чтобы Вы остались довольны,
                                    поэтому перед доставкой отправляем собранный букет на согласование.
                                    Порадуйте своих близких авторскими букетами от Crocus!
                                </p>
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

export default AboutShop;