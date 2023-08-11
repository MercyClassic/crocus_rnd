import { useSearchParams } from 'react-router-dom';


const Search = () => {
    const [searchParams, setSearchParams] = useSearchParams();

    const searchProducts = async (event) => {
        event.preventDefault();
        const searchQuery = event.target.closest('form').search.value;
        if (searchQuery.replace(/\s/g, '').length) {
            setSearchParams({search: searchQuery});
        }
    }

    return(
        <form className="flower__form form-flower">
            <div className="form-flower__search-wrapper">
                <button onClick={(e) => searchProducts(e)} className="form-flower__search-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88 88">
                        <path fill="#b6b6b6"
                            d="M85 31.1c-.5-8.7-4.4-16.6-10.9-22.3C67.6 3 59.3 0 50.6.6c-8.7.5-16.7 4.4-22.5 11-11.2 12.7-10.7 31.7.6 43.9l-5.3 6.1-2.5-2.2-17.8 20 9 8.1 17.8-20.2-2.1-1.8 5.3-6.1c5.8 4.2 12.6 6.3 19.3 6.3 9 0 18-3.7 24.4-10.9 5.9-6.6 8.8-15 8.2-23.7zM72.4 50.8c-9.7 10.9-26.5 11.9-37.6 2.3-10.9-9.8-11.9-26.6-2.3-37.6 4.7-5.4 11.3-8.5 18.4-8.9h1.6c6.5 0 12.7 2.4 17.6 6.8 5.3 4.7 8.5 11.1 8.9 18.2.5 7-1.9 13.8-6.6 19.2z">
                        </path>
                    </svg>
                </button>
                <input name="search" type="text" placeholder="Искать" className="form-flower__search" />
                <button type="reset" className="form-flower__reset-button">
                    <span></span>
                    <span></span>
                </button>
            </div>
            <button onClick={(e) => searchProducts(e)} className="form-flower__button-submit">Найти</button>
        </form>
    );
}

export default Search;
