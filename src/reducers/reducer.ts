export const reducerInitialState = {
  currentPage: 1,

  isGettingConstants: undefined,
  getConstantsFailed: undefined,
  getConstantsSucceeded: undefined,

  isGettingListings: undefined,
  getListingsFailed: undefined,
  getListingsSucceeded: undefined,

  constants: {
    counties: undefined,
    saleDates: undefined,
  },

  data: {
    listings: undefined,
    displayedListings: undefined,
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
          counties: action.constants.counties,
          saleDates: action.constants.saleDates,
        },
      };

    case 'GET_LISTINGS':
      return {
        ...state,
        isGettingListings: true,
        getListingsFailed: false,
        getListingsSucceeded: false,
      };

    case 'GET_LISTINGS_FAILED':
      return {
        ...state,
        isGettingListings: false,
        getListingsFailed: false,
        getListingsSucceeded: true,
      };

    case 'GET_LISTINGS_SUCCEEDED':
      return {
        ...state,
        isGettingListings: false,
        getListingsFailed: false,
        getListingsSucceeded: true,
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
