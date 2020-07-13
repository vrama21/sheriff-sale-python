import React, { useState } from 'react';
import SearchFilters from './SearchFilters';
import useFetch from '../hooks/useFetch';
import Listing from './Listing/Listing';
import ReactLoading from 'react-loading';

const Home = () => {
  // const data = useFetch('/api/table_data', {
  //   method: 'GET',
  //   headers: { 'Content-Type': 'application/json' },
  // });
  const [filters, setFilters] = useState({ county: '', city: '', saleDate: '' });
  const [filteredListings, setFilteredListings] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const listings = useFetch('/api/home', {
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

  const onSubmit = async () => {
    const url = '/api/search';
    const options = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      // body: JSON.stringify(search),
    };

    const response = await fetch(url, options);
    const json = await response.json();
    console.log(json);
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
      {listings && (
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
          <span>Database Last Updated On: {listings.response?.dbModDate}</span>
        </div>
      )}
      <div>
        <SearchFilters
          filters={filters}
          onChange={onFilterChange}
          onSubmit={onSubmit}
          listings={listings.response}
        />
        <Listing listings={listings.response} />
      </div>
    </div>
  );
};

export default Home;
