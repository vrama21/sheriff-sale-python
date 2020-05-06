import React from "react";

const Listing = ({ data }) => (
  <div className="flex flex-wrap">
    {data &&
      data.map((listing, i) => (
        <div className="listing w-1/2" key={`listing-${i}`}>
          <span className="font-bold">{listing.address_sanitized}</span>
          <span className="font-bold">{listing.city}</span>
          <span className="font-bold">{listing.county}</span>
          <span className="font-bold">{listing.sale_date}</span>
        </div>
      ))}
  </div>
);

export default Listing;
