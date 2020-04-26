import React, { useState, useEffect } from 'react';

const useFetch = (url, options = {}) => {
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const resp = await fetch(url, options);
                const json = await resp.json();
                setResponse(json);
            } catch (error) {
                setError(error);
            }
        };

        fetchData();
    }, [options, url]);

    return { response, error };
};

export default useFetch;