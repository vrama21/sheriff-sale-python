import React, { useState, useEffect } from "react";
import SearchFilters from "components/SearchFilters";
import TableData from "components/TableData";
import useFetch from "hooks/useFetch";

const Home = () => {
  const [data, setData] = useState();
  const [filters, setFilters] = useState({});
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState({ county: "" });
  const response = useFetch("/api/home", {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });

  const toggle = () => setIsOpen(!isOpen);

  const onChange = event => {
    const { name, value } = event.target;
    setSearch({
      ...search,
      [name]: value
    });
  };

  const onSubmit = async event => {
    event.preventDefault();
    const url = "/api/table_data";
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(search)
    };

    await fetch(url, options)
      .then(resp => {
        resp.json().then(data => {
          if (data) {
            console.log(data);
            setData(data);
          }
        });
      })
      .catch(err => {
        console.log(err);
      });
  };

  return (
    <>
      <div className="database-container row">
        <div className="col-md-12">
          <div className="database-buttons">
            <button
              type="submit"
              className="btn btn-primary"
              id="check-for-update"
            >
              Check for Updates
            </button>
            <button
              className="btn btn-primary"
              id="update-database"
              // onClick={updateDatabase}
              type="submit"
            >
              Update Database
            </button>
            <button
              className="btn btn-danger"
              id="filters"
              onClick={toggle}
            >
              Filters
            </button>
          </div>
          <span>Database Last Updated On: {}</span>
        </div>
      </div>
      <SearchFilters
        onChange={onChange}
        onSubmit={onSubmit}
        response={response}
        search={search}
      />
      {data && (<TableData data={data} />)}
    </>
  );
};

export default Home;
