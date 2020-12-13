import React, { useState } from 'react';
import Paginate from './Paginate'
import Listing from './Listing'
import { Grid, makeStyles } from '@material-ui/core';

const ListingView = ({ currentPage, listings, pageClick, pageCount }) => {
  const listingsPerPage = 10;
  const indexOfLastBorrower = currentPage * listingsPerPage;
  const indexOfFirstBorrower = indexOfLastBorrower - listingsPerPage;

  const filteredListingsView = listings && listings
    .slice(indexOfFirstBorrower, indexOfLastBorrower)
    .map((listing, listingIndex) => (
      <Listing listing={listing} key={`${listing.address_sanitized}-${listingIndex}`} />
    ))

  return (
    <div style={{ paddingTop: '2rem', margin: '0 3rem' }}>
      <Paginate onClick={pageClick} pageCount={pageCount} />
      {filteredListingsView?.length
        ? <Grid
          container
          direction="row"
          spacing={4}
        >
          {filteredListingsView}
        </Grid>
        : <span>There are no results with the selected filters.</span>
      }
    </div >
  );
};

export default ListingView;