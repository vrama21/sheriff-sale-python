import React, { useEffect, useState } from 'react';
import SearchFilters from '../components/SearchFilters';
import useFetch from '../hooks/useFetch';
import Listing from '../components/Listing/Listing';
import ReactLoading from 'react-loading';

const initialFilterState = { county: '', city: '', saleDate: '' };

export default function Home () {
  const listings = useFetch('/api/listings').response?.listings;
  const initialData = useFetch('/api/home').response?.data;

  const [filters, setFilters] = useState(initialFilterState);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [filteredListings, setFilteredListings] = useState(undefined);

  console.log(initialData);
  console.log(listings);

  const toggle = () => setIsOpen(!isOpen);

  const filterByCounty = (listing) => listing.county === filters.county;
  const filterByCity = (listing) => {
    if (!filters.city) {
      return true;
    }

    return listing.city === filters.city
  }

  const onFilterChange = (event) => {
    const { name, value } = event.target;

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
    if (filtersToApply.length === 0) {
      return
    }

    const listingsWithFilterApplied = listings
      .filter(filterByCounty)
      .filter(filterByCity)

    setFilteredListings(listingsWithFilterApplied);
  };

  useEffect(() => {
    setFilteredListings(listings);
  }, [listings])

  return (
    <div className="container mx-auto">
      {isLoading && (
        <ReactLoading type={"spin"} height={500} width={500} />
      )}
      {initialData && (
        <div className="database-container">
          <div className="database-buttons">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              id="check-for-update"
            >
              Check for Updates
        </button>
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              id="update-database"
              // onClick={updateDatabase}
              type="submit"
            >
              Update Database
              </button>
          </div>
          <span>Database Last Updated On: {initialData.dbModDate}</span>
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
        {filteredListings && <Listing listings={filteredListings} />}
      </div>
    </div>
  );
};
