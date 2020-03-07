import React, { useEffect } from "react";

const TableData = props => {
  useEffect(() => {
    const url = "/api/table_data";
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    };
    
    fetch(url, options)
      .then(resp => {
        resp.json().then(data => {
          console.log(data);
        });
      })
      .catch(err => {
        console.log(err);
      });
  }, []);

  return (
    <table
      id="data-table"
      className="table table-striped table-bordered table-dark"
    >
      <thead>
        <tr>
          <th scope="col">Address</th>
          <th scope="col">City</th>
          <th scope="col">Sale Date</th>
          {/* <!-- <th scope="col">Priors</th> --> */}
          <th scope="col">Plaintiff</th>
          <th id="judgment-col" scope="col">
            Judgment
          </th>
        </tr>
      </thead>
      <tbody id="data-table-body">
        <tr>
          {/* <td>
                        <a href={{ data.maps_url }} target="_blank">
                            {{ data.address_sanitized }}
                            <br>{{ data.unit}}
                            <br>{{ data.secondary_unit }}
                        </a>
                    </td>
                    <td>{{ data.city }}</td>
                    <td>{{ data.sale_date }}</td>
                    <!-- <td>{{ data.priors }}</td> -->
                    <td>{{ data.plaintiff }}</td>
                    <td>{{ data.judgment }}</td>*/}
        </tr>
      </tbody>
    </table>
  );
};

export default TableData;
