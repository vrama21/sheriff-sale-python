import React, { useEffect, useState } from 'react';
import SearchFilters from './SearchFilters';
import useFetch from '../hooks/useFetch';
import Listing from './Listing/Listing';
import ReactLoading from 'react-loading';

const initialFilterState = { county: '', city: '', saleDate: '' };

const Home = () => {
  const listings = useFetch('/api/listings').response?.listings;
  const initialData = useFetch('/api/home').response?.data;

  const [filters, setFilters] = useState(initialFilterState);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [filteredListings, setFilteredListings] = useState(undefined);

  console.log(initialData);
  console.log(listings);

  const toggle = () => setIsOpen(!isOpen);

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
    const countyFilter = listings.filter((listing) => listing.county === filters.county);
    const cityFilter = listings.filter((listing) => listing.city === filters.city);
    setFilteredListings(countyFilter);
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
            <button
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              id="filters"
              onClick={toggle}
            >
              Filters
            </button>
          </div>
          <span>Database Last Updated On: {initialData.response?.dbModDate}</span>
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

export default Home;
