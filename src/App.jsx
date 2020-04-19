import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./components/Home";
import TableData from "./components/TableData"
import "./App.css";

function App() {
  return (
    <div className="container">
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
