import React, { useState } from 'react';
import axios from 'axios';
import SearchFilters from './SearchFilters';
import useFetch from '../hooks/useFetch';
import Listing from './Listing/Listing';
import ReactLoading from 'react-loading';

const initialFilterState = { county: '', city: '', saleDate: '' };

const Home = () => {
  const [filters, setFilters] = useState(initialFilterState);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const [listings, setListings] = useState([]);
  const [filteredListings, setFilteredListings] = useState([]);

  const initialData = useFetch('/api/home', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

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
    setFilters({ county: '', city: '', saleDate: '' });
  };

  const onFilterSubmit = async (event) => {
    event.preventDefault();

    const url = '/api/sheriff_sale';
    const options = {
      body: filters,
    };

    const response = await axios.get(url, options);
    setListings(response.data)
  };

  const updateDatabase = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    const url = '/api/update_database';
    const options = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      data: JSON.stringify(filters),
    };

    await fetch(url, options)
      .then((resp) => {
        resp.json().then((data) => {
          if (data) {
            console.log(data);
            setIsLoading(false);
          }
        });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div className="container mx-auto">
      {initialData && (
        <div className="database-container">
          {isLoading && <ReactLoading type={"spin"} height={500} width={500} />}
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
              onClick={updateDatabase}
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
        <SearchFilters
          filters={filters}
          onFilterChange={onFilterChange}
          onFilterReset={onFilterReset}
          onFilterSubmit={onFilterSubmit}
          initialData={initialData.response}
        />
        {listings && <Listing listings={listings} />}
      </div>
    </div>
  );
};

export default Home;
