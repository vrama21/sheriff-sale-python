//@ts-nocheck
import React from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import {
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from '@material-ui/core';
import useGlobalStyles from '../styles/styles';

const useStyles = makeStyles((theme) => ({
  container: {
    alignItems: 'center',
    display: 'flex',
    justifyContent: 'space-between',
    margin: '1rem 6rem',
  },
}));

const FilterInput = withStyles((theme) => ({
  root: {
    background: theme.palette.grey[500],
    border: '1px solid grey',
    width: 100,
  },
}))(Select);

const FilterLabel = withStyles((theme) => ({
  root: {
    zIndex: 1,
    paddingLeft: '0.5rem'
  },
}))(InputLabel);

export default function SearchFilters({
  filters,
  initialData,
  onFilterChange,
  onFilterReset,
  onFilterSubmit,
}) {
  const globalClasses = useGlobalStyles();
  const classes = useStyles();

  const counties = initialData ? initialData.counties : [];
  const cities = initialData ? initialData.cities : [];
  const citiesOfSelectedCounty =
    initialData && filters.county
      ? Object.keys(initialData.njData[filters.county].cities)
      : [];

  return (
    <div className={classes.container}>
      <div className={classes.container}>
        <Box mt='-10px'>
          <FormControl>
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
        </Box>
        <Box mt='-10px'>
          <FormControl>
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
        </Box>
      </div>

      <div className={classes.container}>
        <Button color="primary" onClick={onFilterSubmit} variant="contained">Submit</Button>
        <Button color="primary" onClick={onFilterReset} variant="contained">Reset</Button>
      </div>
    </div>
  );
}
