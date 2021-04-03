//@ts-nocheck
import React, { useEffect, useState } from 'react';
import SearchFilters from '../components/SearchFilters/SearchFilters';
import useFetch from '../hooks/useFetch';
import ListingView from '../components/ListingView/ListingView';
import { Paper } from '@material-ui/core';
import { ListingInterface } from '../types/types';

const Home = (): React.FC => {
  const listings: ListingInterface[] = useFetch({ url: '/api/get_all_listings', method: 'GET' }).response?.data;
  const initialData = useFetch({ url: '/api/constants', method: 'GET' }).response?.data;

  const initialFilterState = { county: '', city: '', saleDate: '' };

  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState(initialFilterState);
  const [filterErrors, setFilterErrors] = useState(undefined);
  const [filteredListings, setFilteredListings] = useState([]);

  const pageCount = filteredListings && Math.ceil(filteredListings.length / 10);

  const handlePageClick = (data) => setCurrentPage(data.selected + 1);

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

    if (filters === initialFilterState) {
      setFilteredListings(listings);
      return;
    }

    if (!filters.county && filters.county) {
      setFilterErrors({ county: true });
      return;
    }

    const filtersToApply = Object.keys(filters).filter((key) => filters[key]);
    if (filtersToApply.length === 0) {
      setFilteredListings(listings);
    }

    const listingsWithFilterApplied = listings.filter(filterByCounty).filter(filterByCity);

    setCurrentPage(1);
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
        <h1>Sheriff Sale Scraper</h1>
      </div>
      <div>
        <SearchFilters
          cities={initialData?.cities}
          counties={initialData?.counties}
          filters={filters}
          filterErrors={filterErrors}
          njData={initialData?.njData}
          onFilterChange={onFilterChange}
          onFilterReset={onFilterReset}
          onFilterSubmit={onFilterSubmit}
          saleDates={initialData?.saleDates}
        />
        <ListingView currentPage={currentPage} listings={filteredListings} pageClick={handlePageClick} pageCount={pageCount} />
      </div>
    </Paper>
  );
};

export default Home;
