import React from 'react';
import { FormControl, MenuItem } from '@material-ui/core';

import { SearchFiltersProps } from 'types';

import ButtonSubmit from '../ButtonSubmit/ButtonSubmit';
import FilterSelect, { MenuProps } from '../FilterSelect/FilterSelect';
import FilterLabel from '../FilterLabel/FilterLabel';
import { searchFiltersStyles } from './SearchFilters.style';

const SearchFilters: React.FC<SearchFiltersProps> = ({
  counties,
  citiesByCounty,
  filters,
  onFilterChange,
  onFilterReset,
  onFilterSubmit,
  saleDates,
}: SearchFiltersProps) => {
  const classes = searchFiltersStyles();

  const selectedCounty = filters.county;
  const selectedCity = filters.city;
  const selectedSaleDate = filters.saleDate;

  const citiesOfSelectedCounty = citiesByCounty?.[selectedCounty]?.cities || [];

  const countyMenuItems = counties?.map((county) => (
    <MenuItem key={`county-${county}`} value={county}>
      {county}
    </MenuItem>
  ));

  const cityMenuItems = citiesOfSelectedCounty?.map((city) => (
    <MenuItem key={`city-${city}`} value={city}>
      {city}
    </MenuItem>
  ));

  const saleDateMenuItems = saleDates?.map((saleDate) => (
    <MenuItem key={`saleDate-${saleDate}`} value={saleDate}>
      {saleDate}
    </MenuItem>
  ));

  return (
    <div>
      <div className={classes.filterContainer}>
        <FormControl className={classes.filterSelect}>
          <FilterLabel id="county-select-label">County</FilterLabel>
          <FilterSelect
            children={countyMenuItems}
            id="county-select"
            labelId="county-select-label"
            MenuProps={MenuProps}
            name="county"
            onChange={onFilterChange}
            value={selectedCounty || ''}
            variant="outlined"
          />
        </FormControl>
        <FormControl className={classes.filterSelect}>
          <FilterLabel>City</FilterLabel>
          <FilterSelect
            children={cityMenuItems}
            id="city-select"
            MenuProps={MenuProps}
            name="city"
            onChange={onFilterChange}
            value={selectedCity || ''}
            variant="outlined"
          />
        </FormControl>
        <FormControl className={classes.filterSelect}>
          <FilterLabel>Sale Date</FilterLabel>
          <FilterSelect
            children={saleDateMenuItems}
            id="sale-date-select"
            MenuProps={MenuProps}
            name="saleDate"
            onChange={onFilterChange}
            value={selectedSaleDate || ''}
            variant="outlined"
          />
        </FormControl>
      </div>

      <div>
        <ButtonSubmit name="submit" onClick={onFilterSubmit} value="Submit" />
        <ButtonSubmit name="reset" onClick={onFilterReset} value="Reset" />
      </div>
    </div>
  );
};

export default SearchFilters;
