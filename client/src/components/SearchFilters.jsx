import React from "react";
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';

const FilterInput = withStyles({
  root: {
    // background: 'white',
    border: 1,
    borderRadius: 3,
    padding: 10,
    width: 100,
  },
})(Select);

const useStyles = makeStyles((theme) => ({
  margin: {
    margin: theme.spacing(1),
  },
}));

export default function SearchFilters({
  filters,
  initialData,
  onFilterChange,
  onFilterReset,
  onFilterSubmit,
}) {
  const classes = useStyles();

  const counties = initialData ? initialData.counties : [];
  const cities = initialData ? initialData.cities : [];

  const citiesOfSelectedCounty = initialData && filters.county ? Object.keys(initialData?.njData[filters?.county].cities) : [];

  return (
    <div className="filter-container">
      <div className="flex justify-center mt-5">
        <FormControl className={classes.margin}>
          <InputLabel id="county-select-label">County</InputLabel>
          <FilterInput
            id="county-select"
            labelId="county-select-label"
            name="county"
            onChange={onFilterChange}
            value={filters.county || ''}
          >
            <MenuItem value=''>
              <em>None</em>
            </MenuItem>
            {counties.map((county, i) => (
              <MenuItem
                key={`county-${i}`}
                value={county}
              >
                {county}
              </MenuItem>
            ))}
          </FilterInput>
        </FormControl>
        <FormControl className={classes.margin}>
          <InputLabel>City</InputLabel>
          <FilterInput
            id="city-select"
            name="city"
            onChange={onFilterChange}
            value={filters.city || ''}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {citiesOfSelectedCounty
              ? citiesOfSelectedCounty.map((city, i) => (
                <MenuItem
                  key={`city-${i}`}
                  value={city}
                >
                  {city}
                </MenuItem>
              ))
              : cities.map((city, i) => (
                <MenuItem
                  key={`city-${i}`}
                  value={city}
                >
                  {city}
                </MenuItem>
              ))}
          </FilterInput>
        </FormControl>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={onFilterSubmit}
          type="submit"
        >
          Submit
        </button>
        <button
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          id="filter-reset"
          onClick={onFilterReset}
        >
          Reset
        </button>
      </div>
    </div >
  );
};
