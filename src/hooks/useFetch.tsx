import { useState, useEffect } from 'react';

interface useFetchProps {
  url: string;
  method: string;
  options?: Record<string, unknown>;
}

interface useFetchType {
  response: Record<string, unknown>[];
  error: string | null | undefined;
}

const useFetch = ({ url, method, options }: useFetchProps): useFetchType => {
  const [response, setResponse] = useState(undefined);
  const [error, setError] = useState(undefined);

  useEffect(() => {
    const defaultOption = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };

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
