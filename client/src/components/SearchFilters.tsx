import React from "react";
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';

const FilterInput = withStyles({
  root: {
    background: 'white',
    border: 1,
    borderRadius: 3,
    padding: 10,
    width: 100,
  },
})(Select);

const FilterLabel = withStyles({
  root: {
    color: 'black',
    marginLeft: '0.5rem',
    zIndex: 1,
  },
})(InputLabel);

const useStyles = makeStyles((theme) => ({
  button: {
    background: '#4299e1',
    borderRadius: '0.25rem',
    color: 'white',
    fontWeight: 700,
    padding: '0.5rem 1rem',

    '&:hover': {
      background: '#2b6cb0'
    },
  },
  container: {
    alignItems: 'center',
    display: 'flex',
    justifyContent: 'space-between',
    margin: '1rem 3rem',
  },
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

  const citiesOfSelectedCounty = initialData && filters.county ? Object.keys(initialData.njData[filters.county].cities) : [];

  return (
    <div className={classes.container}>
      <div>
        <FormControl className={classes.margin}>
          <FilterLabel id="county-select-label">County</FilterLabel>
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
          <FilterLabel>City</FilterLabel>
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
                <MenuItem key={`city-${i}`} value={city}>
                  {city}
                </MenuItem>
              ))
              : cities.map((city, i) => (
                <MenuItem key={`city-${i}`} value={city}>
                  {city}
                </MenuItem>
              ))}
          </FilterInput>
        </FormControl>
      </div>

      <div>
        <button
          className={classes.button}
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
    </div>
  );
};
