import React, { useContext } from 'react';
import Paginate from '../Paginate/Paginate';
import Listing from '../Listing/Listing';
import Loading from '../Loading/Loading';
import ListingTable from '../ListingTable/ListingTable';
import { Grid } from '@material-ui/core';
import { ListingInterface } from '../../types';
import { ListingViewStyles } from './ListingView.styles';
import { AppContext } from '../../App';

interface ListingViewProps {
  listings: Record<string, undefined>[];
}

const ListingView: React.FC<ListingViewProps> = ({ listings }: ListingViewProps) => {
  const classes = ListingViewStyles();
  const { state } = useContext(AppContext);

  const { currentPage } = state;
  const listingsPerPage = 25;
  const indexOfLastBorrower = currentPage * listingsPerPage;
  const indexOfFirstBorrower = indexOfLastBorrower - listingsPerPage;
  const pageCount = listings && Math.ceil(listings.length / listingsPerPage);

  const filteredListingsView = listings?.slice(indexOfFirstBorrower, indexOfLastBorrower);

  return (
    <div className={classes.root}>
      {filteredListingsView?.length > 0 && (
        <div>
          <Paginate pageCount={pageCount} />
          <ListingTable listings={filteredListingsView} />
        </div>
      )}
      {filteredListingsView?.length === 0 && <span>There are no results with the selected filters.</span>}
    </div>
  );
};

export default ListingView;
