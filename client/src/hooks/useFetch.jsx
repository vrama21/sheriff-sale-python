import { useState, useEffect } from 'react';

const useFetch = (url, options = {}) => {
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const resp = await fetch(url, options);
                const json = await resp.json();
                setIsLoading(true);
                setResponse(json);
            } catch (error) {
                setError(error);
            }
        };

        setIsLoading(false);
        fetchData();
    }, []);

    return { response, error, isLoading };
};

export default useFetch;