//@ts-nocheck
import React from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import { Button, FormControl, InputLabel, MenuItem, Select } from '@material-ui/core';
import ButtonSubmit from '../ButtonSumbit/ButtonSubmit';
import ResetSubmit from '../ResetSubmit/ResetSubmit';

const useStyles = makeStyles((theme) => ({
  container: {
    margin: '1rem',
  },
}));

const FilterFormControl = withStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.grey[700],
    margin: '0 0.5rem',
    width: 225,
  },
}))(FormControl);

const FilterSelect = withStyles((theme) => ({
  root: {
    border: '1px solid grey',
    fontWeight: 'bold',
    paddingBottom: '1rem',
  },
}))(Select);

const FilterLabel = withStyles((theme) => ({
  root: {
    color: 'white',
    fontWeight: 'bold',
    paddingLeft: '0.5rem',
    position: 'absolute',
    zIndex: 1,
  },
  focused: {
    color: theme.palette.primary.light,
  },
}))(InputLabel);

const MenuProps = {
  anchorOrigin: {
    vertical: 'bottom',
    horizontal: 'left',
  },
  transformOrigin: {
    vertical: 'top',
    horizontal: 'left',
  },
  getContentAnchorEl: null,
};

const SearchFilters = ({ filters, filterErrors, initialData, onFilterChange, onFilterReset, onFilterSubmit }) => {
  const classes = useStyles();

  const counties = initialData?.counties || [];
  const cities = initialData?.cities || [];
  const citiesOfSelectedCounty = filters.county ? Object.keys(initialData?.njData[filters.county].cities) : [];
  const saleDates = initialData?.saleDates || [];

  const countyMenuItems = counties.map((county) => (
    <MenuItem key={`county-${county}`} value={county}>
      {county}
    </MenuItem>
  ));

  const cityMenuItems = citiesOfSelectedCounty
    ? citiesOfSelectedCounty.map((city, cityIndex) => (
        <MenuItem key={`city-${city}-${cityIndex}`} value={city}>
          {city}
        </MenuItem>
      ))
    : cities.map((city, cityIndex) => (
        <MenuItem key={`city-${city}-${cityIndex}`} value={city}>
          {city}
        </MenuItem>
      ));

  const saleDateMenuItems = saleDates.map((saleDate) => (
    <MenuItem key={`saleDate-${saleDate}`} value={saleDate}>
      {saleDate}
    </MenuItem>
  ));

  return (
    <div className={classes.container}>
      <div className={classes.container}>
        <FilterFormControl>
          <FilterLabel id="county-select-label">County</FilterLabel>
          <FilterSelect
            children={countyMenuItems}
            id="county-select"
            labelId="county-select-label"
            MenuProps={MenuProps}
            name="county"
            onChange={onFilterChange}
            value={filters.county || ''}
            variant="outlined"
          />
        </FilterFormControl>
        <FilterFormControl>
          <FilterLabel>City</FilterLabel>
          <FilterSelect
            children={cityMenuItems}
            id="city-select"
            MenuProps={MenuProps}
            name="city"
            onChange={onFilterChange}
            value={filters.city || ''}
            variant="outlined"
          />
        </FilterFormControl>
        <FilterFormControl>
          <FilterLabel>Sale Date</FilterLabel>
          <FilterSelect
            children={saleDateMenuItems}
            id="sale-date-select"
            MenuProps={MenuProps}
            name="saleDate"
            onChange={onFilterChange}
            value={filters.saleDate || ''}
            variant="outlined"
          />
        </FilterFormControl>
      </div>

      <div className={classes.container}>
        <ButtonSubmit onClick={onFilterSubmit} />
        <ResetSubmit onClick={onFilterReset} />
      </div>
    </div>
  );
};

export default SearchFilters;
