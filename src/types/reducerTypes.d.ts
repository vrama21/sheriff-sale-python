import { ListingInterface } from '../types/types';

export interface Reducer {
  currentPage: number;

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
    counties: Record<string, Record<'cities', string[]>> | undefined;
    saleDates: string[] | [] | undefined;
  };

  data: {
    filteredListings: any[];
    listing: ListingInterface;
    listings: ListingInterface[] | any[];
  };
}
