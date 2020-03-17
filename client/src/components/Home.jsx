import React, { useState, useEffect } from "react";
import SearchFilters from "./SearchFilters";
import TableData from "./TableData";
import "./style.css";

const Home = props => {
  const [response, setResponse] = useState({});
  const [dbModDate, setDbModDate] = useState();
  const [search, setSearch] = useState({});
  const [filters, setFilters] = useState({});
  const [data, setData] = useState();

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
      method: "POST",
      headers: { "Content-Type": "text/plain" }
    };
    fetch(url, options)
      .then(resp => {
        resp.json().then(data => {
          console.log(data);
        });
      })
      .catch(err => {
        console.log(err);
      });
  };

  const handleChange = event => {
    const { name, value } = event.target;
    setSearch({
      ...search,
      [name]: value
    });
  };

  const handleSubmit = async event => {
    event.preventDefault();
    const url = "/api/table_data";
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(search)
    };

    await fetch(url, options)
      .then(resp => {
        resp.json().then(data => {
          if (data) {
            console.log(data);
            setData(data);
          }
        });
      })
      .catch(err => {
        console.log(err);
      });
  };

  const toggleChecked = () => {
    // setFilters({
    //   ...filters,
    //   [name]: setChecked(prev => !prev)
    // });
    setFilters((prevState, divName) => ({
      ...prevState,
      [divName]: !prevState
    }));
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
      <SearchFilters
        response={response}
        handleChange={handleChange}
        handleSubmit={handleSubmit}
        toggleChecked={toggleChecked}
      />
      {data && <TableData data={data} />}
    </>
  );
};

export default Home;
