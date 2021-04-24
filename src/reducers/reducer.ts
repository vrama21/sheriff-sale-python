export const reducerInitialState = {
  currentPage: 1,

  isGettingConstants: undefined,
  getConstantsFailed: undefined,
  getConstantsSucceeded: undefined,

  isGettingListing: undefined,
  getListingFailed: undefined,
  getListingSucceeded: undefined,

  isGettingAllListings: undefined,
  getAllListingsFailed: undefined,
  getAllListingsSucceeded: undefined,

  constants: {
    counties: undefined,
    saleDates: undefined,
  },

  data: {
    listing: undefined,
    listings: undefined,
    filteredListings: [],
  },
};

export const reducer = (state = reducerInitialState, action) => {
  switch (action.type) {
    case 'GET_CONSTANTS':
      return {
        ...state,
        isGettingConstants: true,
        getConstantsFailed: false,
        getConstantsSucceeded: false,
      };

    case 'GET_CONSTANTS_FAILED':
      return {
        ...state,
        isGettingConstants: false,
        getConstantsFailed: false,
        getConstantsSucceeded: true,
      };

    case 'GET_CONSTANTS_SUCCEEDED':
      return {
        ...state,
        isGettingConstants: false,
        getConstantsFailed: false,
        getConstantsSucceeded: true,
        constants: {
          ...state.constants,
          counties: action.counties,
          saleDates: action.saleDates,
        },
      };

    case 'GET_LISTING':
      return {
        ...state,
        isGettingListing: true,
        getListingFailed: false,
        getListingSucceeded: false,
      };

    case 'GET_LISTING_FAILED':
      return {
        ...state,
        isGettingListing: false,
        getListingFailed: true,
        getListingSucceeded: false,
        data: {
          ...state.data,
          listing: {},
        },
      };

    case 'GET_LISTING_SUCCEEDED':
      return {
        ...state,
        isGettingAllListings: false,
        getAllListingsFailed: false,
        getAllListingsSucceeded: true,
        data: {
          ...state.data,
          listing: action.listing,
        },
      };

    case 'GET_ALL_LISTINGS':
      return {
        ...state,
        isGettingAllListings: true,
        getAllListingsFailed: false,
        getAllListingsSucceeded: false,
      };

    case 'GET_ALL_LISTINGS_FAILED':
      return {
        ...state,
        isGettingAllListings: false,
        getAllListingsFailed: true,
        getAllListingsSucceeded: false,
      };

    case 'GET_ALL_LISTINGS_SUCCEEDED':
      return {
        ...state,
        isGettingAllListings: false,
        getAllListingsFailed: false,
        getAllListingsSucceeded: true,
        data: {
          ...state.data,
          listings: action.listings,
        },
      };

    case 'SET_PAGE':
      return {
        ...state,
        currentPage: action.currentPage,
      };

    default:
      return state;
  }
};
