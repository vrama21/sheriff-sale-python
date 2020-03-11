import React from "react";
import "./style.css";

const SearchFilters = props => (
  <div className="filter-container row">
    <form method="POST" onSubmit={props.handleSubmit}>
      <div className="input-group col-md-12">
        <div className="input-group-prepend">
          <label className="input-group-text">County</label>
          <select
            className="custom-select"
            name="county"
            onChange={props.handleChange}
          >
            <option value="">--Choose--</option>
            {props.response.counties &&
              props.response.counties.map((county, i) => (
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
            onChange={props.handleChange}
          >
            <option value="">--Choose--</option>
            {props.response.cities &&
              props.response.cities.map((city, i) => (
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
            onChange={props.handleChange}
          >
            <option value="">--Choose--</option>
            {props.response.saleDates &&
              props.response.saleDates.map((saleDate, i) => (
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

export default SearchFilters;
