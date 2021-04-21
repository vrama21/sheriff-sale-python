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
  dispatch({ type: 'GET_ALL_LISTINGS' });

  try {
    const allListings = await request({ url: '/api/get_all_listings', method: 'GET' });

    dispatch({ listings: allListings.data, type: 'GET_ALL_LISTINGS_SUCCEEDED' });
  } catch (err) {
    console.error('getAllListings error: ', err);

    dispatch({ type: 'GET_ALL_LISTINGS_FAILED' });
  }
};

export const getListing = async ({ listingId, dispatch }: { listingId: string; dispatch: Dispatch }): Promise<void> => {
  dispatch({ type: 'GET_LISTING' });

  try {
    const listing = await request({ url: `/api/get_listing/${listingId}`, method: 'GET' });

    dispatch({ listing: listing.data, type: 'GET_LISTING_SUCCEEDED' });
  } catch (err) {
    console.error('getListing error: ', err);

    dispatch({ type: 'GET_LISTING_FAILED' });
  }
};
