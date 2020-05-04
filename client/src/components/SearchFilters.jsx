import React from "react";
// import { FormGroup, FormControlLabel, Switch } from "@material-ui/core";

const SearchFilters = ({ onChange, onSubmit, response, search }) => {
  const counties = response && response.counties;
  const cities = response && response.cities;
  const saleDates = response && response.saleDates;

  return (
    <div className="container mx-auto text-center">
      <form method="POST" onSubmit={onSubmit}>
        <div className="flex">
          <div className="select-group">
            <label className="select-label">County</label>
            <select
              className="select-styled"
              name="county"
              onChange={onChange}
            >
              <option value="">--Choose--</option>
              {response && counties.map((county, i) => (
                <option
                  className="select-options"
                  key={`county-${i}`}
                  value={county}
                >
                  {county}
                </option>
              ))}
            </select>
          </div>
          <div className="select-group">
            <label className="select-label">City</label>
            <select
              className=""
              name="city"
              onChange={onChange}
            >
              <option value="">--Choose--</option>
              {cities && cities.map((city, i) => (
                <option key={`city-${i}`} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>
          <div className="input-group-prepend">
            <label className="select-label">Sale Date</label>
            <select
              className=""
              name="sale_date"
              onChange={onChange}
            >
              <option value="">--Choose--</option>
              {saleDates && saleDates.map((saleDate, i) => (
                <option key={`saleDate-${i}`} value={saleDate}>
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
