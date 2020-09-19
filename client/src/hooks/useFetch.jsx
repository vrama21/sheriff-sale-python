import { useState, useEffect } from 'react';

const useFetch = (url, method, options) => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const defaultOption = {
      method,
      headers: { 'Content-Type': 'application/json' }
    }

    const fetchData = async () => {
      try {
        const resp = await fetch(url, options || defaultOption);
        const json = await resp.json();
        setResponse(json);
      } catch (error) {
        setError(error);
      }
    };

    fetchData();
  }, [method, options, url]);

  return { response, error };
};

export default useFetch;
