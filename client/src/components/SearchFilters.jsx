import React, { useEffect } from "react";
import { makeStyles, withStyles, StylesProvider } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';

const FilterInput = withStyles({
  root: {
    border: 1,
    borderRadius: 3,
    padding: 15,
    width: 100,
  }
})(Select);

const useStyles = makeStyles((theme) => ({
  margin: {
    margin: theme.spacing(1),
  },
}));

export default function SearchFilters({
  filters,
  listings,
  onChange,
  onSubmit,
}) {
  const classes = useStyles();
  const countyCities = listings && filters.county ? Object.keys(listings?.njData[filters?.county].cities) : undefined;

  return (
    <div className="filter-container">
      <div className="flex justify-center mt-5">
        <form method="POST" onSubmit={onSubmit}>
          <FormControl className={classes.margin}>
            <InputLabel id="county-select-label">County</InputLabel>
            <FilterInput
              id="county-select"
              labelId="county-select-label"
              name="county"
              onChange={onChange}
            >
              <MenuItem value=''>
                <em>None</em>
              </MenuItem>
              {listings?.counties.map((county, i) => (
                <MenuItem
                  key={`county-${i}`}
                  value={county || ''}
                >
                  {county}
                </MenuItem>
              ))}
            </FilterInput>
          </FormControl>
          <FormControl className={classes.margin}>
            <InputLabel>City</InputLabel>
            <Select
              id="city-select"
              name="city"
              onChange={onChange}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {filters?.county
                ? countyCities.map((city, i) => (
                  <MenuItem
                    key={`city-${i}`}
                    value={city}
                  >
                    {city}
                  </MenuItem>
                ))
                : listings?.cities.map((city, i) => (
                  <MenuItem
                    key={`city-${i}`}
                    value={city}
                  >
                    {city}
                  </MenuItem>
                ))}
            </Select>
          </FormControl>
          <FormControl className={classes.margin}>
            <InputLabel>Sale Date</InputLabel>
            <Select
              id="saleDate-select"
              name="saleDate"
              onChange={onChange}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {listings?.saleDates.map((saleDate, i) => (
                <MenuItem
                  key={`saleDate-${i}`}
                  value={saleDate}
                >
                  {saleDate}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
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
        </form>
      </div>
    </div >
  );
};
