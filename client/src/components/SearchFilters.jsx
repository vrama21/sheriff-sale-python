import React from "react";
import CheckboxInput from "components/Checkbox/Checkbox";

const SearchFilters = ({ onChange, onFilterChange, onSubmit, response }) => {
  const counties = response?.counties;
  const cities = response?.cities;
  const saleDates = response?.saleDates;

  return (
    <div className="bg-white">
      <CheckboxInput
        label="Judgement"
        name="judgement"
        onChange={onFilterChange}
      />
      <div className="flex justify-center mt-5">
        <form method="POST" onSubmit={onSubmit}>
          <div>
            <div className="select-group mx-4 bg-gray-400 hover:bg-gray-500">
              <label className="mr-4">County</label>
              <select
                className="select-styled"
                name="county"
                onChange={onChange}
              >
                <option value="">--Choose--</option>
                {counties.map((county, i) => (
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
            <div className="select-group mx-4 bg-gray-400 hover:bg-gray-500">
              <label className="mr-4">City</label>
              <select className="select-styled" name="city" onChange={onChange}>
                <option value="">--Choose--</option>
                {cities.map((city, i) => (
                  <option key={`city-${i}`} value={city}>
                    {city}
                  </option>
                ))}
              </select>
            </div>
            <div className="select-group mx-4 bg-gray-400 hover:bg-gray-500">
              <label className="mr-4">Sale Date</label>
              <select
                className="select-styled"
                name="sale_date"
                onChange={onChange}
              >
                <option value="">--Choose--</option>
                {saleDates.map((saleDate, i) => (
                  <option key={`saleDate-${i}`} value={saleDate}>
                    {saleDate}
                  </option>
                ))}
              </select>
            </div>
            <input
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              type="submit"
              value="Submit"
            />
            <button
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
              id="filter-reset"
            >
              Reset
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SearchFilters;
