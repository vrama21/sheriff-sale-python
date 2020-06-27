import React, { useState } from 'react';
import SearchFilters from './SearchFilters';
import useFetch from '../hooks/useFetch';
import Listing from './Listing/Listing';
import ReactLoading from 'react-loading';

const Home = () => {
  const data = useFetch('/api/table_data', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  const [filters, setFilters] = useState({ county: undefined, city: undefined, saleDate: undefined });
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const listings = useFetch('/api/home', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  const toggle = () => setIsOpen(!isOpen);

  const onChange = (event) => {
    const { name, value } = event.target;
    setSearch({
      ...search,
      [name]: value,
    });
  };

  const onFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters({ ...filters, [name]: value });
  };

  const updateDatabase = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    const url = '/api/update_database';
    const options = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      data: JSON.stringify(search),
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
      <SearchFilters
        filters={filters}
        onChange={onChange}
        onFilterChange={onFilterChange}
        // onSubmit={onSubmit}
        response={listings.response}
        search={search}
      />
      <Listing data={data.response} />
    </div>
  );
};

export default Home;
