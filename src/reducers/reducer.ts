export const reducerInitialState = {
  currentPage: 1,
  isGettingListings: undefined,
  getListingsFailed: undefined,
  getListingsSucceeded: undefined,
  data: {
    listings: undefined,
    displayedListings: undefined,
  },
};

export const reducer = (state = reducerInitialState, action) => {
  switch (action.type) {
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
