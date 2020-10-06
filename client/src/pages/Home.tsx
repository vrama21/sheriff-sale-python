import React, { useEffect, useState } from 'react';
import SearchFilters from '../components/SearchFilters';
import useFetch from '../hooks/useFetch';
import ListingView from '../components/ListingView';
import * as types from '../types/types';
import useGlobalStyles from '../styles/styles';
import { Button, makeStyles, Paper } from '@material-ui/core';

const initialFilterState = { county: '', city: '', saleDate: '' };

const useStyles = makeStyles(() => ({
  listingContainerStyle: {
    borderRadius: '1rem',
  },
}));

const Home = () => {
  const listings = useFetch('/api/listings', 'GET').response?.listings;
  const initialData = useFetch('/api/home', 'GET').response?.data;

  const [filters, setFilters] = useState<types.Filter>(initialFilterState);
  const [filterErrors, setFilterErrors] = useState(undefined);
  // const [isLoading, setIsLoading] = useState<boolean>(false);
  const [filteredListings, setFilteredListings] = useState<types.Listing[]>([]);
  const pageCount = filteredListings && Math.ceil(filteredListings.length / 10);

  const filterByCounty = (listing: types.Listing) => listing.county === filters.county;

  const filterByCity = (listing: types.Listing) => {
    if (!filters.city) {
      return true;
    }

    return listing.city === filters.city;
  };

  const onFilterChange = (event: types.ButtonEvent): void => {
    const { name, value }: { name: string; value: string } = event.target;

    if (name === 'county') {
      setFilters({ county: value, city: '', saleDate: '' });
      return;
    }

    setFilters({ ...filters, [name]: value });
  };

  const onFilterReset = (): void => {
    setFilters(initialFilterState);
  };

  const onFilterSubmit = (): void => {
    if (!listings) {
      return;
    }

    if (filters === initialFilterState) {
      setFilteredListings(listings);
      return;
    }

    const filtersToApply = Object.keys(filters).filter((key) => filters[key]);
    if (filtersToApply.length === 0) {
      setFilteredListings(listings);
    }

    const listingsWithFilterApplied = listings
      .filter(filterByCounty)
      .filter(filterByCity);

    setFilteredListings(listingsWithFilterApplied);
  };

  useEffect(() => {
    setFilteredListings(listings);
  }, [listings]);

  const globalClasses = useGlobalStyles();
  const classes = useStyles();

  return (
    <Paper
      elevation={0}
      style={{
        height: '115vh',
        padding: '1rem 0',
        textAlign: 'center',
      }}
    >
      {initialData && (
        <div style={{ padding: '0.5rem 0' }}>
          <Button
            color="primary"
            variant="contained"
            style={{ margin: '0 1rem' }}
          >
            {' '}
            Check for Updates{' '}
          </Button>
          <Button
            color="secondary"
            variant="contained"
            style={{ margin: '0 1rem' }}
          >
            {' '}
            Update Database{' '}
          </Button>
          {/* <span>Database Last Updated On: {initialData.dbModDate}</span> */}
        </div>
      )}
      <div>
        {initialData && (
          <SearchFilters
            filters={filters}
            filterErrors={filterErrors}
            onFilterChange={onFilterChange}
            onFilterReset={onFilterReset}
            onFilterSubmit={onFilterSubmit}
            initialData={initialData}
          />
        )}
        <ListingView listings={filteredListings} pageCount={pageCount} />
      </div>
    </Paper>
  );
};

export default Home;
