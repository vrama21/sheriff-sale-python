import React, { useState, useEffect } from "react";
import SearchFilters from "./SearchFilters";
import "./style.css";

const Home = () => {
  const [response, setResponse] = useState({});
  const [dbModDate, setDbModDate] = useState();

  useEffect(() => {
    const url = "/api/home";
    const options = {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    };
    fetch(url, options)
      .then(resp => {
        resp.json().then(data => {
          console.log(data);
          setResponse({
            counties: data.counties,
            cities: data.cities,
            saleDates: data.saleDates
          });
          setDbModDate(data.dbModDate);
        });
      })
      .catch(err => {
        console.log(err);
      });
  }, []);

  const updateDatabase = () => {
    const url = "/api/update_database";
    const options = {
      method: "PUT",
      headers: { "Content-Type": "text/plain" }
    };
    fetch(url, options)
      .then(resp => {
        console.log(resp);
      })
      .catch(err => {
        console.log(err);
      });
  };

  return (
    <>
      <div className="database-container row">
        <div className="col-md-12">
          <div className="database-buttons">
            <button
              type="submit"
              className="btn btn-primary"
              id="check-for-update"
            >
              Check for Updates
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              id="update-database"
              onClick={updateDatabase}
            >
              Update Database
            </button>
          </div>
          <span>Database Last Updated On: {dbModDate}</span>
        </div>
      </div>
      <SearchFilters response={response} />
    </>
  );
};

export default Home;
