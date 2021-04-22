import { ConstantsResponse } from 'types';

interface requestProps {
  url: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  options?: Record<string, unknown>;
}

interface RequestType {
  data: ConstantsResponse;
}

/**
 * Creates an http request to an url
 */
const request = async ({ url, method, options }: requestProps): Promise<RequestType> => {
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

export default request;
