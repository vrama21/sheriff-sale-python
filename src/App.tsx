import React, { useReducer } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';
import { reducer, reducerInitialState } from './reducers/reducer';

export const AppContext = React.createContext({});

export const AppProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, reducerInitialState);

  return <AppContext.Provider value={{ state, dispatch }}>{children}</AppContext.Provider>;
};

const App: React.FC = () => (
  <AppProvider>
    <div>
      <Router>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
        </Switch>
      </Router>
    </div>
  </AppProvider>
);

export default App;
