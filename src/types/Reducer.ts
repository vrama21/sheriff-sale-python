import { Listing } from 'types';

export interface Reducer {
  currentPage: number | undefined;

  isGettingConstants: boolean | undefined;
  getConstantsFailed: boolean | undefined;
  getConstantsSucceeded: boolean | undefined;

  isGettingListing: boolean | undefined;
  getListingFailed: boolean | undefined;
  getListingSucceeded: boolean | undefined;

  isGettingAllListings: boolean | undefined;
  getAllListingsFailed: boolean | undefined;
  getAllListingsSucceeded: boolean | undefined;

  constants: {
    counties: string[] | undefined;
    saleDates: string[] | [] | undefined;
  };

  data: {
    filteredListings: Listing[];
    listing: Listing | undefined;
    listings: Listing[] | undefined;
  };
}
