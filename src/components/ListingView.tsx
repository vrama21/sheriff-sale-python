import React from 'react';
import Paginate from './Paginate'
import Listing from './Listing'
import { Grid } from '@material-ui/core';

const ListingView = ({ currentPage, listings, pageClick, pageCount }) => {
  const listingsPerPage = 10;
  const indexOfLastBorrower = currentPage * listingsPerPage;
  const indexOfFirstBorrower = indexOfLastBorrower - listingsPerPage;

  const filteredListingsView = listings?.slice(indexOfFirstBorrower, indexOfLastBorrower)
    .map((listing, listingIndex) => (
      <Listing listing={listing} key={`${listing.address_sanitized}-${listingIndex}`} />
    ))

  return (
    <div style={{ paddingTop: '2rem', margin: '0 3rem' }}>
      {(pageCount || pageCount > 0) && <Paginate onClick={pageClick} pageCount={pageCount} />}
      {filteredListingsView?.length
        ? <Grid
          container
          direction="row"
          spacing={4}
        >
          {filteredListingsView}
        </Grid>
        : <span>
          There are no results with the selected filters.
        </span>
      }
    </div >
  );
};

export default ListingView;