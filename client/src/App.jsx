import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';
import TableData from './components/TableData';

export default function App () {
  return (
    <div>
      <Router>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route exact path="/table_data">
            <TableData />
          </Route>
        </Switch>
      </Router>
    </div>
  );
};
