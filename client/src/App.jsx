import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./components/Home";
import TableData from "./components/TableData"

function App() {
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
}

export default App;
