import React, { useEffect, useState } from 'react';
import SearchFilters from '../components/SearchFilters';
import useFetch from '../hooks/useFetch';
import Listing from '../components/Listing';
import * as types from '../types/types'
import useGlobalStyles from '../styles/styles';
import Button from '../components/Button';
import { Paper } from '@material-ui/core';

const initialFilterState = { county: '', city: '', saleDate: '' };

const Home = () => {
  const listings = useFetch('/api/listings', 'GET').response?.listings;
  const initialData = useFetch('/api/home', 'GET').response?.data;

  const [filters, setFilters] = useState<types.Filter>(initialFilterState);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [filteredListings, setFilteredListings] = useState<types.EnumeratedArrayOfObjects>([]);

  const filterByCounty = (listing) => listing.county === filters.county;
  const filterByCity = (listing) => {
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
      // @ts-ignore
      setFilteredListings(listings);
    }
    const listingsWithFilterApplied = listings
      // @ts-ignore
      .filter(filterByCounty)
      .filter(filterByCity)

    // @ts-ignore
    setFilteredListings(listingsWithFilterApplied);
  };

  useEffect(() => {
    // @ts-ignore
    setFilteredListings(listings);
  }, [listings])

  const globalClasses = useGlobalStyles();


  return (
    // @ts-ignore
    <Paper>
      {initialData && (
        <div>
          <div>
            <Button text="Check for Updates" />
            <Button text="Update Database" />
          </div>
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
            // @ts-ignore
            filteredListings.map((listing) => (
              <Listing listing={listing} />
            ))
          )}
        </div>
      </div>
    </Paper>
  );
};

export default Home;
