import request from '../helpers/request';
import { Dispatch } from '../types/types';

export const getConstants = async (dispatch: Dispatch): Promise<void> => {
  dispatch({ type: 'GET_CONSTANTS' });

  try {
    const constants = await request({ url: '/api/constants', method: 'GET' });

    dispatch({ constants: constants.data, type: 'GET_CONSTANTS_SUCCEEDED' });
  } catch (err) {
    console.error('getConstants error: ', err);

    dispatch({ type: 'GET_CONSTANTS_FAILED' });
  }
};

export const getAllListings = async (dispatch: Dispatch): Promise<void> => {
  dispatch({ type: 'GET_LISTINGS' });

  try {
    const allListings = await request({ url: '/api/get_all_listings', method: 'GET' });

    dispatch({ listings: allListings.data, type: 'GET_LISTINGS_SUCCEEDED' });
  } catch (err) {
    console.error('getAllListings error: ', err);

    dispatch({ type: 'GET_LISTINGS_FAILED' });
  }
};
