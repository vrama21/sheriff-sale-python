import React, { useContext, useEffect, useState } from 'react';
import SearchFilters from '../../components/SearchFilters/SearchFilters';
import ListingView from '../../components/ListingView/ListingView';
import { Paper } from '@material-ui/core';
import { ListingInterface } from '../../types/types';
import { homePageStyles } from './HomePage.style';
import { getConstants, getAllListings } from '../../actions/actions';
import { AppContext } from '../../App';
import { isEqual } from 'lodash';

const HomePage: React.FC = () => {
  const classes = homePageStyles();
  const { state, dispatch } = useContext(AppContext);

  const hasGottenConstants = state.getConstantsSucceeded === true;
  const hasGottenListings = state.getAllListingsSucceeded === true;

  const counties = state?.constants?.counties && Object.keys(state?.constants?.counties);
  const citiesByCounty = state?.constants?.counties && state?.constants?.counties;
  const saleDates = hasGottenConstants && state?.constants?.saleDates;

  const listings = state.data.listings;

  const initialFilterState = { county: undefined, city: undefined, saleDate: undefined };

  const [filters, setFilters] = useState(initialFilterState);
  const [filteredListings, setFilteredListings] = useState(undefined);

  const filterByCounty = (listing: ListingInterface) => (filters.county ? listing.county === filters.county : true);
  const filterByCity = (listing: ListingInterface) => (filters.city ? listing.city === filters.city : true);
  const filterBySaleDate = (listing: ListingInterface) => (filters.saleDate ? listing.sale_date === filters.saleDate : true);

  const onFilterReset = () => {
    setFilters(initialFilterState);
    setFilteredListings(listings);
  };

  const onFilterChange = (event) => {
    const { name, value } = event.target;

    setFilters({ ...filters, [name]: value });
  };

  const onFilterSubmit = () => {
    if (!listings) {
      return;
    }

    dispatch({ type: 'SET_PAGE', currentPage: 1 });

    if (isEqual(filters, initialFilterState)) {
      setFilteredListings(listings);

      return;
    }

    const filtersToApply = Object.keys(filters).filter((key) => filters[key]);
    if (filtersToApply.length === 0) {
      setFilteredListings(listings);
    }

    const listingsWithFilterApplied = listings.filter(filterByCounty).filter(filterByCity).filter(filterBySaleDate);

    setFilteredListings(listingsWithFilterApplied);
  };

  useEffect(() => {
    if (!hasGottenListings || listings.length === 0) {
      getAllListings(dispatch);
    }

    if (!hasGottenConstants) {
      getConstants(dispatch);
    }
  }, [dispatch, hasGottenConstants, hasGottenListings, listings]);

  return (
    <Paper className={classes.root} elevation={0}>
      <div className={classes.header}>
        <div className={classes.title}>
          <h1>Sheriff Sale Scraper</h1>
        </div>
        <div>
          {hasGottenConstants && (
            <SearchFilters
              counties={counties}
              citiesByCounty={citiesByCounty}
              filters={filters}
              onFilterChange={onFilterChange}
              onFilterReset={onFilterReset}
              onFilterSubmit={onFilterSubmit}
              saleDates={saleDates}
            />
          )}
        </div>
      </div>
      <ListingView listings={filteredListings || listings} />
    </Paper>
  );
};

export default HomePage;
