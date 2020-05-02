import React from "react";
// import { FormGroup, FormControlLabel, Switch } from "@material-ui/core";

const SearchFilters = ({ onChange, onSubmit, response, search }) => {
  const cities = search.county ? Object.keys(response.NJData[search.county].Cities) : response.cities;

  return (
    <div className="filter-container row">
      <form method="POST" onSubmit={onSubmit}>
        <div className="input-group col-md-12">
          <div className="input-group-prepend">
            <label className="input-group-text">County</label>
            <select
              className="custom-select"
              name="county"
              onChange={onChange}
            >
              <option value="">--Choose--</option>
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
              onChange={onChange}
            >
              <option value="">--Choose--</option>

              {cities && cities.map((city, i) => (
                <option key={`city-${i}`} value={city}>
                  {city}
                </option>
              ))
              }
            </select>
          </div>
          <div className="input-group-prepend">
            <label className="input-group-text">Sale Date</label>
            <select
              className="custom-select"
              name="sale_date"
              onChange={onChange}
            >
              <option value="">--Choose--</option>
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
      <div className="col-md-12">
        {/* <FormGroup>
        <FormControlLabel
          control={<Switch />}
          onChange={toggleChecked}
          label="Judgment"
          name="judgmentFilter"
        />
      </FormGroup> */}
      </div>
    </div>
  );
};

export default SearchFilters;
