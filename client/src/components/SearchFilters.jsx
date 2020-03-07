import React, { useState } from "react";
import { Redirect } from "react-router-dom";
import "./style.css";

const SearchFilters = ({ response }) => {
  const [searchParams, setSearchParams] = useState({});

  const handleChange = event => {
    const { name, value } = event.target;
    setSearchParams({
      ...searchParams,
      [name]: value
    });
  };

  const handleSubmit = async event => {
    event.preventDefault();
    const url = "/api/table_data";
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(searchParams)
    };

    await fetch(url, options)
      .then(resp => {
        resp.json().then(data => {
          console.log(data);
          return <Redirect to="/table_data" />;
        });
      })
      .catch(err => {
        console.log(err);
      });
  };

  return (
    <div className="filter-container row">
      <form method="POST" onSubmit={handleSubmit}>
        <div className="input-group col-md-12">
          <div className="input-group-prepend">
            <label className="input-group-text">County</label>
            <select
              className="custom-select"
              name="county"
              onChange={handleChange}
            >
              {response.counties &&
                response.counties.map((county, i) => (
                  <option key={i} value={county}>
                    {county}
                  </option>
                ))}
            </select>
          </div>
          <div className="input-group-prepend">
            <label className="input-group-text">City</label>
            <select
              className="custom-select"
              name="city"
              onChange={handleChange}
            >
              {response.cities &&
                response.cities.map((city, i) => (
                  <option key={i} value={city}>
                    {city}
                  </option>
                ))}
            </select>
          </div>
          <div className="input-group-prepend">
            <label className="input-group-text">Sale Date</label>
            <select
              className="custom-select"
              name="sale_date"
              onChange={handleChange}
            >
              {response.saleDates &&
                response.saleDates.map((saleDate, i) => (
                  <option key={i} value={saleDate}>
                    {saleDate}
                  </option>
                ))}
            </select>
          </div>
          <input
            className="btn btn-primary col-md-1"
            type="submit"
            value="Submit"
          ></input>
          <button id="filter-reset" className="btn btn-secondary col-md-1">
            Reset
          </button>
        </div>
      </form>
    </div>
  );
};

export default SearchFilters;
