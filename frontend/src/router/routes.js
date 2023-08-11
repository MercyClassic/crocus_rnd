import {Navigate} from 'react-router-dom';
import AboutShop from '../pages/AboutShop';
import ContactInformation from '../pages/ContactInformation';
import PrivacyPolicy from '../pages/PrivacyPolicy';
import ProductDetail from '../pages/ProductDetail';
import NotFound from '../pages/NotFound';
import Products from '../pages/Products';


const routes = [
    {path: '/', element: <Products />, exact: true},
    {path: '/flower/:slug', element: <ProductDetail />, exact: true},
    {path: '/favourites', element: <Products favourites={true} />, exact: true},
    {path: '/about_shop', element: <AboutShop />, exact: true},
    {path: '/privacy_policy', element: <PrivacyPolicy />, exact: true},
    {path: '/contact_information', element: <ContactInformation />, exact: true},
    {path: '/not_found', element: <NotFound />, exact: true},
    {path: '*', element: <Navigate replace to='/not_found' />},
]

export default routes;
