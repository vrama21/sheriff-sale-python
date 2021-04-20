import React, { useReducer } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';
import { reducer, reducerInitialState } from './reducers/reducer';
import { Dispatch } from './types/types';
import { Reducer } from './reducers/reducer.types';
import { LoadScript } from '@react-google-maps/api';

export const AppContext = React.createContext<{
  state: Reducer;
  dispatch: Dispatch;
}>({
  state: reducerInitialState,
  dispatch: () => null,
});

export const AppProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, reducerInitialState);

  return <AppContext.Provider value={{ state, dispatch }}>{children}</AppContext.Provider>;
};

const App: React.FC = () => (
  <LoadScript googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY}>
    <AppProvider>
      <Router>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
        </Switch>
      </Router>
    </AppProvider>
  </LoadScript>
);

export default App;
