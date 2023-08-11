import {useState} from 'react';


const useFetching = (callback) => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState({});

    const fetching = async () => {
        try {
            setIsLoading(true);
            await callback();
        } catch (e) {
            setError(e.request);
        } finally {
            setIsLoading(false);
        }
    }

    return [fetching, isLoading, error]
}

export default useFetching;
