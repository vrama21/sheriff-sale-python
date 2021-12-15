import React, { useReducer } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { LoadScript } from '@react-google-maps/api';

import HomePage from 'pages/HomePage/HomePage';
import ListingPage from 'pages/ListingPage/ListingPage';
import { reducer, reducerInitialState } from 'reducers/reducer';
import { Action, Reducer } from 'types';

import { globalStyles } from 'styles/styles';

type GlobalContent = {
  state: Reducer;
  dispatch: React.Dispatch<Action>;
};

export const AppContext = React.createContext<GlobalContent>({
  state: reducerInitialState,
  dispatch: () => null,
});

export const AppProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, reducerInitialState);

  return <AppContext.Provider value={{ state, dispatch }}>{children}</AppContext.Provider>;
};

const App: React.FC = () => {
  const classes = globalStyles();

  return (
    <div className={classes.container}>
      <LoadScript googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY as string}>
        <AppProvider>
          <Router>
            <Switch>
              <Route exact path="/" component={HomePage}></Route>
              <Route path="/listing/:listingId" component={ListingPage}></Route>
            </Switch>
          </Router>
        </AppProvider>
      </LoadScript>
    </div>
  );
};

export default App;
