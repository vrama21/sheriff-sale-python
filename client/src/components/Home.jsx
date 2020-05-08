import React, { useState, useEffect } from "react";
import SearchFilters from "components/SearchFilters";
import useFetch from "hooks/useFetch";
import Listing from "components/Listing/Listing";

const initialFilterState = {
  judgement: true,
};

const Home = () => {
  const [filters, setFilters] = useState(initialFilterState);
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState(undefined);
  const listings = useFetch("/api/home", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  const toggle = () => setIsOpen(!isOpen);

  const onChange = (event) => {
    const { name, value } = event.target;
    setSearch({
      ...search,
      [name]: value,
    });
  };

  const onFilterChange = (event, valueOverride) => {
    const { name } = event.target;
    setFilters({ ...filters, [name]: valueOverride });
  };

  const updateDatabase = async (event) => {
    event.preventDefault();
    const url = "/api/update_database";
    const options = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };

    await fetch(url, options)
      .then((resp) => {
        resp.json().then((data) => {
          if (data) {
            console.log(data);
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
      {isOpen && (
        <SearchFilters
          onChange={onChange}
          onFilterChange={onFilterChange}
          // onSubmit={onSubmit}
          response={listings.response}
          search={search}
        />
      )}
      <Listing data={listings.response?.tableData} />
    </div>
  );
};

export default Home;
