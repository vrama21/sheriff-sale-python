import React, { useState } from 'react';
import Paginate from './Paginate'
import Listing from './Listing'
import { Grid } from '@material-ui/core';
import * as types from '../types/types';
import useGlobalStyles from '../styles/styles';

interface ListingViewInterface {
  currentPage: number,
  listings: any,
  pageClick: any,
  pageCount: any,
}

const ListingView = ({ currentPage, listings, pageClick, pageCount }: ListingViewInterface) => {
  const listingsPerPage = 10;
  // const [currentPage, setCurrentPage] = useState(1);
  const indexOfLastBorrower = currentPage * listingsPerPage;
  const indexOfFirstBorrower = indexOfLastBorrower - listingsPerPage;

  const filteredListingsView = listings && listings
    .slice(indexOfFirstBorrower, indexOfLastBorrower)
    .map((listing: types.Listing, listingIndex: number) => (
      <Grid item xs={12} key={`${listing.address_sanitized}-${listingIndex}`}>
        <Listing listing={listing} />
      </Grid>
    ))

  const globalClasses = useGlobalStyles();

  return (
    <div>
      <Paginate onClick={pageClick} pageCount={pageCount} />
      <div className={globalClasses.container}>
        {filteredListingsView?.length ? filteredListingsView : 'There are no results with the selected filters'}
      </div>
    </div >
  );
};

export default ListingView;