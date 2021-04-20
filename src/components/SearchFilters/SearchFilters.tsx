import React from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import { FormControl, InputLabel, MenuItem } from '@material-ui/core';
import ButtonSubmit from '../ButtonSumbit/ButtonSubmit';
import ResetSubmit from '../ResetSubmit/ResetSubmit';
import { SearchFiltersProps } from '../../types';
import { FilterSelect, MenuProps } from '../FilterSelect/FilterSelect';

const useStyles = makeStyles((theme) => ({
  filterContainer: {
    margin: '1rem',
  },
  filterSelect: {
    backgroundColor: theme.palette.grey[700],
    margin: '0 0.5rem',
    width: 225,
  },
}));

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

const SearchFilters: React.FC<SearchFiltersProps> = ({
  counties,
  citiesByCounty,
  filters,
  filterErrors,
  onFilterChange,
  onFilterReset,
  onFilterSubmit,
  saleDates,
}: SearchFiltersProps) => {
  const classes = useStyles();

  console.log(counties, filters.county)
  const citiesOfSelectedCounty: string[] = filters.county ? citiesByCounty[filters.county]['cities'] : [];

  const countyMenuItems = counties?.map((county) => (
    <MenuItem key={`county-${county}`} value={county}>
      {county}
    </MenuItem>
  ));

  const cityMenuItems = citiesOfSelectedCounty?.map((city, cityIndex) => (
    <MenuItem key={`city-${city}-${cityIndex}`} value={city}>
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
            value={filters.county || ''}
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
            value={filters.city || ''}
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
            value={filters.saleDate || ''}
            variant="outlined"
          />
        </FormControl>
      </div>

      <div>
        <ButtonSubmit onClick={onFilterSubmit} />
        <ResetSubmit onClick={onFilterReset} />
      </div>
    </div>
  );
};

export default SearchFilters;
