export const reducerInitialState = {
  currentPage: 1,
};

export const reducer = (state = reducerInitialState, action) => {
  switch (action.type) {
    case 'SET_PAGE':
      return {
        ...state,
        currentPage: action.currentPage,
      };
    default:
      return state;
  }
};
