interface fetchApiProps {
  url: string;
  method: string;
  options?: Record<string, unknown>;
}

interface fetchApiType {
  data: Record<string, unknown>[] | undefined;
}

const fetchApi = async ({ url, method, options }: fetchApiProps): Promise<fetchApiType> => {
  const defaultOption = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };

  try {
    const response = (await fetch(url, options || defaultOption)).json();

    return response;
  } catch (err) {
    console.error('useFetch failed with: ', err);
  }
};

export default fetchApi;
