import { Dispatch } from 'types';
import { DateTime } from 'luxon';

import request from 'helpers/request';

export const getConstants = async (dispatch: Dispatch): Promise<void> => {
  dispatch({ type: 'GET_CONSTANTS' });

  try {
    const constants = await request({ url: '/api/get_constants', method: 'GET' });

    const { counties, saleDates } = constants.data;

    const saleDateTimes = saleDates.map((saleDate) => DateTime.fromFormat(saleDate, 'm/d/yyyy'));

    const currentMonth = DateTime.local().month;
    const currentYear = DateTime.local().year;

    const filteredSaleDates = saleDateTimes
      .filter((saleDateTime) => saleDateTime.month <= currentMonth + 1 && saleDateTime.year === currentYear)
      .map((saleDateTime) => saleDateTime.toFormat('m/d/yyyy'));

    dispatch({ counties, saleDates: filteredSaleDates, type: 'GET_CONSTANTS_SUCCEEDED' });
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
