//@ts-nocheck
import React from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import Button from '../components/Button';
import useStyles from '../styles/styles';

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
  const citiesOfSelectedCounty =
    initialData && filters.county
      ? Object.keys(initialData.njData[filters.county].cities)
      : [];

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
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {counties.map((county: string, countyIndex: number) => (
              <MenuItem key={`county-${countyIndex}`} value={county}>
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
              ? citiesOfSelectedCounty.map((city: string, cityIndex: number) => (
                <MenuItem key={`city-${cityIndex}`} value={city}>
                  {city}
                </MenuItem>
              ))
              : cities.map((city: string, cityIndex: number) => (
                <MenuItem key={`city-${cityIndex}`} value={city}>
                  {city}
                </MenuItem>
              ))}
          </FilterInput>
        </FormControl>
      </div>

      <div>
        <Button onClick={onFilterSubmit} text="Submit" />
        <Button onClick={onFilterReset} text="Reset" />
      </div>
    </div>
  );
}
