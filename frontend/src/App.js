import React, { useState } from 'react';
import './static/style.css';
import { BrowserRouter } from 'react-router-dom';
import AppRouter from './components/AppRouter';
import { CountCartProductsContext } from './context';


function App() {
    const [countCartProducts, setCountCartProducts] = useState(0);

    return(
        <CountCartProductsContext.Provider value={{
            countCartProducts,
            setCountCartProducts,
        }}>
            <BrowserRouter>
                <AppRouter />
            </BrowserRouter>
        </CountCartProductsContext.Provider>
    );
}

export default App;
