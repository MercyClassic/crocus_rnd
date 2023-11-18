import {Link} from 'react-router-dom';
import CallMe from '../functions/CallMe';
import {useState} from 'react';
import Loader from '../components/Loader';
import formatPhoneNumber from '../functions/formatPhoneNumber';


const Delivery = () => {
    const [loader, isLoading] = useState(false);

    const createCallMe = async (event) => {
        isLoading(true);
        await CallMe(event);
        isLoading(false);
    }

    return(
        <>
        {loader && <Loader />}
        <section className="delivery">
            <img src="/static/img/jpg/bg.jpg" className="delivery__background" />
            <div className="delivery__body">
                <h1 className="delivery__title"> <p> Доставка <span style={{display: 'block'}}> свежих цветов </span> </p> <span>в Ростове-на-Дону</span></h1>
                <p className="delivery__text">
                    <span style={{display: 'block', borderBottom: "none"}}> Не можете определиться c выбором? </span>
                    Закажите <span> <Link style={{color: "inherit"}} href="tel: +7 (918) 521-25-71"> онлайн звонок бесплатно </Link> </span>
                </p>
                <form className="delivery__form" method="post" action="/api/v1/call_me">
                    <input onClick={(e) => formatPhoneNumber(e)} name="phone_number" placeholder="+7 (999) 999 99-99" type="text" className="delivery__number-input" required maxLength="20" minLength="11" />
                    <button onClick={(e) => createCallMe(e)} className="delivery__number-button">Перезвоните мне</button>
                </form>
                <Link to="/" className="delivery__button">Весь каталог</Link>
            </div>
        </section>
        </>
    );
}

export default Delivery;
