//@ts-nocheck
import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';

export const AuthContext = React.createContext();

const App = () => (
  <AuthContext.Provider>
    <div>
      <Router>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
        </Switch>
      </Router>
    </div>
  </AuthContext.Provider>
);

export default App;
