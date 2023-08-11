import { Routes, Route } from 'react-router-dom';
import routes from '../router/routes';


const AppRouter = () => {
    return(
        <Routes>
            {routes.map((route) =>
                <Route path={route.path} element={route.element} exact={route.exact} key={route.path}/>
            )}
        </Routes>
    );
}

export default AppRouter;
