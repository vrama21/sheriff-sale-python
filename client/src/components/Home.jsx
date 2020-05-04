import React, { useState, useEffect } from "react";
import SearchFilters from "components/SearchFilters";
import TableData from "components/TableData";
import useFetch from "hooks/useFetch";


const Home = () => {
  const [data, setData] = useState(undefined);
  const [filters, setFilters] = useState(undefined);
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState(undefined);
  const { response } = useFetch("/api/home", {
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

  const updateDatabase = async (event) => {
    event.preventDefault();
    const url = "/api/update_database";
    const options = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      data: JSON.stringify(search),
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

  const onSubmit = async (event) => {
    event.preventDefault();
    const url = "/api/table_data";
    const options = {
      method: "POST",
      // headers: { "Content-Type": "application/json" },
      body: JSON.stringify(search),
    };

    await fetch(url, options)
      .then((resp) => {
        resp.json().then((data) => {
          if (data) {
            console.log(data);
            setData(data);
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
        <span>Database Last Updated On: {response && response.dbModDate}</span>
      </div>
      <SearchFilters
        onChange={onChange}
        onSubmit={onSubmit}
        response={response}
        search={search}
      />
      {data && <TableData data={data} />}
    </div>
  );
};

export default Home;
