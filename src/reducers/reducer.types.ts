import { ListingInterface } from '../types/types';

export interface Reducer {
  currentPage: number;

  isGettingConstants: boolean | undefined;
  getConstantsFailed: boolean | undefined;
  getConstantsSucceeded: boolean | undefined;

  isGettingListings: boolean | undefined;
  getListingsFailed: boolean | undefined;
  getListingsSucceeded: boolean | undefined;

  constants: {
    counties: Record<string, Record<'cities', string[]>> | undefined;
    saleDates: string[] | [] | undefined;
  };

  data: {
    filteredListings: any[];
    listings: ListingInterface[] | any[];
  };
}
