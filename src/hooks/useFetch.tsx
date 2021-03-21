import { useState, useEffect } from 'react';

const useFetch = (url: string, method: string, options?: object) => {
  const [response, setResponse] = useState(undefined);
  const [error, setError] = useState(undefined);

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
