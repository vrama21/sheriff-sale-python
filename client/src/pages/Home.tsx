// @ts-nocheck
import React, { useEffect, useState } from 'react';
import SearchFilters from '../components/SearchFilters';
import useFetch from '../hooks/useFetch';
import ListingView from '../components/ListingView';
import * as types from '../types/types';
import { Button, Paper } from '@material-ui/core';

const initialFilterState = { county: '', city: '', saleDate: '' };

const Home = () => {
  const listings = useFetch('/api/listings', 'GET').response?.listings;
  const initialData = useFetch('/api/home', 'GET').response?.data;

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [filters, setFilters] = useState<types.Filter>(initialFilterState);
  const [filterErrors, setFilterErrors] = useState(undefined);
  // const [isLoading, setIsLoading] = useState<boolean>(false);
  const [filteredListings, setFilteredListings] = useState<types.Listing[]>([]);

  const pageCount = filteredListings && Math.ceil(filteredListings.length / 10);

  const handlePageClick = (data: { selected: number }) => {
    setCurrentPage(data.selected + 1);
  };

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

    if (!filters.county && filters.county) {
      // @ts-ignore
      setFilterErrors({ county: true })
      return;
    }

    const filtersToApply = Object.keys(filters).filter((key) => filters[key]);
    if (filtersToApply.length === 0) {
      setFilteredListings(listings);
    }

    const listingsWithFilterApplied = listings
      .filter(filterByCounty)
      .filter(filterByCity);

    setCurrentPage(1)
    setFilteredListings(listingsWithFilterApplied);

  };

  useEffect(() => {
    setFilteredListings(listings);
  }, [listings]);

  return (
    <Paper
      elevation={0}
      style={{
        height: '115vh',
        padding: '1rem 0',
        textAlign: 'center',
      }}
    >
      <div style={{ padding: '0.5rem 0' }}>
        <Button
          color="primary"
          variant="contained"
          size='large'
          style={{ fontWeight: 'bold', margin: '0 1rem' }}
        >
          Check for Updates
          </Button>
        <Button
          color="secondary"
          variant="contained"
          size='large'
          style={{ fontWeight: 'bold', margin: '0 1rem' }}
        >
          Update Database
          </Button>
      </div>
      <span>Database Last Updated On: {initialData?.dbModDate}</span>
      <div>
        <SearchFilters
          filters={filters}
          filterErrors={filterErrors}
          onFilterChange={onFilterChange}
          onFilterReset={onFilterReset}
          onFilterSubmit={onFilterSubmit}
          initialData={initialData}
        />
        <ListingView
          currentPage={currentPage}
          listings={filteredListings}
          pageClick={handlePageClick}
          pageCount={pageCount}
        />
      </div>
    </Paper>
  );
};

export default Home;
