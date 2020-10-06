import React, { useEffect, useState } from 'react';
import SearchFilters from '../components/SearchFilters';
import useFetch from '../hooks/useFetch';
import Listing from '../components/Listing';
import * as types from '../types/types'
import useGlobalStyles from '../styles/styles';
import { Button, Grid, makeStyles, Paper } from '@material-ui/core';

const initialFilterState = { county: '', city: '', saleDate: '' };

const useStyles = makeStyles(() => ({
  listingContainerStyle: {
    borderRadius: '1rem',
  }
}))

const Home = () => {
  const listings = useFetch('/api/listings', 'GET').response?.listings;
  const initialData = useFetch('/api/home', 'GET').response?.data;

  const [filters, setFilters] = useState<types.Filter>(initialFilterState);
  // const [isLoading, setIsLoading] = useState<boolean>(false);
  const [filteredListings, setFilteredListings] = useState<types.Listing[]>([]);

  const filterByCounty = (listing: types.Listing) => listing.county === filters.county;
  const filterByCity = (listing: types.Listing) => {
    if (!filters.city) {
      return true;
    }

    return listing.city === filters.city
  }

  const onFilterChange = (event: types.ButtonEvent): void => {
    const { name, value }: { name: string, value: string } = event.target;

    if (name === 'county') {
      setFilters({ county: value, city: '', saleDate: '' })
      return;
    }

    setFilters({ ...filters, [name]: value });
  };

  const onFilterReset = () => {
    setFilters(initialFilterState);
  };

  const onFilterSubmit = () => {
    if (!listings) {
      return;
    }

    const filtersToApply = Object.keys(filters).filter((key) => filters[key]);
    console.log(filtersToApply)
    if (filtersToApply.length === 0) {
      setFilteredListings(listings);
    }
    const listingsWithFilterApplied = listings
      .filter(filterByCounty)
      .filter(filterByCity)

    setFilteredListings(listingsWithFilterApplied);
  };

  useEffect(() => {
    setFilteredListings(listings);
  }, [listings])

  const globalClasses = useGlobalStyles();
  const classes = useStyles();

  return (
    <Paper style={{ height: '100vh', textAlign: "center" }}>
      {initialData && (
        <div style={{ padding: '0.5rem 0' }}>
          <Button color='primary' variant='contained' style={{ margin: '0 1rem' }}> Check for Updates </Button>
          <Button color='secondary' variant='contained' style={{ margin: '0 1rem' }}> Update Database </Button>
          {/* <span>Database Last Updated On: {initialData.dbModDate}</span> */}
        </div>
      )}
      <div>
        {initialData && (
          <SearchFilters
            filters={filters}
            onFilterChange={onFilterChange}
            onFilterReset={onFilterReset}
            onFilterSubmit={onFilterSubmit}
            initialData={initialData}
          />
        )}
        <div className={globalClasses.container}>
          {filteredListings && (
            <Grid className={classes.listingContainerStyle} container>
              {filteredListings.map((listing: types.Listing, listingIndex: number) => (
                <Grid item xs={12} key={`${listing.address_sanitized}-${listingIndex}`}>
                  <Listing listing={listing} />
                </Grid>
              ))}
            </Grid>
          )}
        </div>
      </div>
    </Paper>
  );
};

export default Home;
