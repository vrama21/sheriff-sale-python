import React, { useContext } from 'react';

import { AppContext } from 'App';
import { ListingInterface } from 'types';

import Paginate from '../Paginate/Paginate';
import ListingTable from '../ListingTable/ListingTable';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';
import { listingViewStyles } from './ListingView.styles';

interface ListingViewProps {
  listings: ListingInterface[];
}

const ListingView: React.FC<ListingViewProps> = ({ listings }: ListingViewProps) => {
  const classes = listingViewStyles();
  const { state } = useContext(AppContext);

  const { currentPage } = state;
  const listingsPerPage = 25;
  const indexOfLastBorrower = currentPage * listingsPerPage;
  const indexOfFirstBorrower = indexOfLastBorrower - listingsPerPage;
  const pageCount = listings && Math.ceil(listings.length / listingsPerPage);
  const viewableListings = listings && listings.slice(indexOfFirstBorrower, indexOfLastBorrower);

  return (
    <div className={classes.listingViewContainer}>
      {listings && (
        <div>
          <Paginate pageCount={pageCount} />
          <ListingTable listings={viewableListings} />
        </div>
      )}
      {!listings && <LoadingSpinner />}
      {viewableListings?.length === 0 && <span>There are no results with the selected filters.</span>}
    </div>
  );
};

export default ListingView;
