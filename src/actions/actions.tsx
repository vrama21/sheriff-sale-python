import fetch from '../helpers/fetch';
import { Dispatch } from '../types/types';

export const getAllListings = async (dispatch: Dispatch): Promise<void> => {
  dispatch({ type: 'GET_LISTINGS' });

  try {
    const allListings = await fetch({ url: '/api/get_all_listings', method: 'GET' });

    dispatch({ listings: allListings.data, type: 'GET_LISTINGS_SUCCEEDED' });
  } catch (err) {
    console.error('getAllListings error: ', err);

    dispatch({ type: 'GET_LISTINGS_FAILED' });
  }
};
