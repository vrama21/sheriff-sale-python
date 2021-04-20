import React, { useContext, useEffect, useState } from 'react';
import SearchFilters from '../components/SearchFilters/SearchFilters';
import ListingView from '../components/ListingView/ListingView';
import { Paper } from '@material-ui/core';
import { ListingInterface } from '../types/types';
import { homePageStyles } from './Home.style';
import { getConstants, getAllListings } from '../actions/actions';
import { AppContext } from '../App';
import { isEqual } from 'lodash';

const Home: React.FC = () => {
  const { state, dispatch } = useContext(AppContext);

  const hasGottenConstants = state.getConstantsSucceeded === true;
  const hasGottenListings = state.getListingsSucceeded === true;

  const classes = homePageStyles();
  const counties = state?.constants?.counties && Object.keys(state?.constants?.counties);
  const citiesByCounty = state?.constants?.counties && state?.constants?.counties;
  const saleDates = hasGottenConstants && Object.keys(state?.constants?.saleDates);

  const listings = state.data.listings;

  const initialFilterState = { county: undefined, city: undefined, saleDate: undefined };

  const [filters, setFilters] = useState(initialFilterState);
  const [filteredListings, setFilteredListings] = useState(undefined);

  const filterByCounty = (listing: ListingInterface) => listing.county === filters.county;

  const filterByCity = (listing: ListingInterface) => {
    if (!filters.city) {
      return true;
    }

    return listing.city === filters.city;
  };

  const onFilterChange = (event) => {
    const { name, value } = event.target;

    if (name === 'county') {
      setFilters({ county: value, city: '', saleDate: '' });
      return;
    }

    setFilters({ ...filters, [name]: value });
  };

  const onFilterReset = () => setFilters(initialFilterState);

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

    const listingsWithFilterApplied = listings.filter(filterByCounty).filter(filterByCity);

    setFilteredListings(listingsWithFilterApplied);
  };

  useEffect(() => {
    if (!hasGottenListings) {
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

export default Home;
