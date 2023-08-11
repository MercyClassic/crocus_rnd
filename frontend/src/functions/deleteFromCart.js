import ProductService from '../API/ProductService';


const deleteFromCart = async (target) => {
    const toDelete = target.closest('li');
    const toDeleteSlug = toDelete.querySelector('input').dataset.slug;
    await ProductService.addToSession(toDeleteSlug, 'cart');
    toDelete.remove();
}

export default deleteFromCart;
