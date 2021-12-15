import React, { useContext, useEffect, useState } from 'react';
import { Paper } from '@material-ui/core';
import { isEqual } from 'lodash';

import { AppContext } from 'App';
import { getConstants, getAllListings } from 'actions/actions';
import { Listing } from 'types';

import SearchFilters from 'components/SearchFilters/SearchFilters';
import ListingView from 'components/ListingView/ListingView';
import { homePageStyles } from './HomePage.style';

const HomePage: React.FC = () => {
  const classes = homePageStyles();
  const { state, dispatch } = useContext(AppContext);

  const hasGottenConstants = state.getConstantsSucceeded === true;
  const hasGottenListings = state.getAllListingsSucceeded === true;

  const counties = (state.constants.counties && Object.keys(state.constants.counties)) as string[];
  const citiesByCounty = state.constants.counties;
  const listings = state.data.listings;
  const saleDates = state.constants.saleDates;

  const initialFilterState = { county: undefined, city: undefined, saleDate: undefined };

  const [filters, setFilters] = useState(initialFilterState);
  const [filteredListings, setFilteredListings] = useState(undefined);

  const filterByCounty = (listing: Listing) => (filters.county ? listing.county === filters.county : true);
  const filterByCity = (listing: Listing) => (filters.city ? listing.city === filters.city : true);
  const filterBySaleDate = (listing: Listing) => (filters.saleDate ? listing.sale_date === filters.saleDate : true);

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
