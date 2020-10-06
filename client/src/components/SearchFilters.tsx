//@ts-nocheck
import React from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import {
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

const FilterFormControl = withStyles((theme) => ({
  root: {
    marginTop: '-10px',
  }
}))(FormControl);

const FilterSelect = withStyles((theme) => ({
  root: {
    background: theme.palette.grey[700],
    border: '1px solid grey',
    width: 100,
  },
  selectMenu: {
    top: '150px',
  }
}))(Select);

const FilterLabel = withStyles((theme) => ({
  root: {
    fontWeight: 'bold',
    paddingLeft: '0.5rem',
    zIndex: 1,
  },
}))(InputLabel);

const SearchFilters = ({
  filters,
  filterErrors,
  initialData,
  onFilterChange,
  onFilterReset,
  onFilterSubmit,
}) => {
  const classes = useStyles();

  const counties = initialData ? initialData.counties : [];
  const cities = initialData ? initialData.cities : [];
  const citiesOfSelectedCounty =
    initialData && filters.county
      ? Object.keys(initialData.njData[filters.county].cities)
      : [];

  const countyMenuItems = counties.map((county: string, countyIndex: number) => (
    <MenuItem key={`county-${countyIndex}`} value={county}>
      {county}
    </MenuItem>
  ));

  const cityMenuItems = citiesOfSelectedCounty
    ? citiesOfSelectedCounty.map((city: string, cityIndex: number) => (
      <MenuItem key={`city-${cityIndex}`} value={city}>
        {city}
      </MenuItem>
    ))
    : cities.map((city: string, cityIndex: number) => (
      <MenuItem key={`city-${cityIndex}`} value={city}>
        {city}
      </MenuItem>
    ))

  return (
    <div className={classes.container}>
      <div className={classes.container}>
        <FilterFormControl>
          <FilterLabel id="county-select-label">County</FilterLabel>
          <FilterSelect
            children={countyMenuItems}
            id="county-select"
            labelId="county-select-label"
            name="county"
            onChange={onFilterChange}
            value={filters.county || ''}
          />
        </FilterFormControl>
        <FilterFormControl>
          <FilterLabel>City</FilterLabel>
          <FilterSelect
            children={cityMenuItems}
            id="city-select"
            name="city"
            onChange={onFilterChange}
            value={filters.city || ''}
          />
        </FilterFormControl>
      </div>

      <div className={classes.container}>
        <Button color="primary" onClick={onFilterSubmit} variant="contained">Submit</Button>
        <Button color="secondary" onClick={onFilterReset} variant="contained">Reset</Button>
      </div>
    </div>
  );
}

export default SearchFilters;