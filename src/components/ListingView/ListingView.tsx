import React from 'react';
import Paginate from '../Paginate/Paginate';
import Listing from '../Listing/Listing';
import Loading from '../Loading/Loading';
import { Grid } from '@material-ui/core';
import { ListingInterface } from '../../types';
import { reducer, reducerInitialState } from '../../reducers/reducer';

interface ListingViewProps {
  currentPage: number;
  listings: Record<string, undefined>[];
  pageCount: number;
}

const ListingView: React.FC<ListingViewProps> = ({ listings }: ListingViewProps) => {
  const [state, dispatch] = React.useReducer(reducer, reducerInitialState);
  const { currentPage } = state;
  const listingsPerPage = 10;
  const indexOfLastBorrower = currentPage * listingsPerPage;
  const indexOfFirstBorrower = indexOfLastBorrower - listingsPerPage;
  const pageCount = listings && Math.ceil(listings.length / 10);

  const filteredListingsView = listings
    ?.slice(indexOfFirstBorrower, indexOfLastBorrower)
    .map((listing: ListingInterface, listingIndex: number) => (
      <Listing
        address={listing.address}
        attorney={listing.attorney}
        attorney_phone={listing.attorney_phone}
        city={listing.city}
        defendant={listing.defendant}
        judgment={listing.judgment}
        latitude={parseFloat(listing.latitude)}
        longitude={parseFloat(listing.longitude)}
        maps_url={listing.maps_url}
        plaintiff={listing.plaintiff}
        priors={listing.priors}
        sale_date={listing.sale_date}
        state={listing.state}
        street={listing.street}
        zip_code={listing.zip_code}
        key={`${listing.address_sanitized}-${listingIndex}`}
      />
    ));

  return (
    <div style={{ paddingTop: '2rem', margin: '0 3rem' }}>
      {(currentPage || currentPage > 0) && <Paginate pageCount={pageCount} />}
      {!filteredListingsView && <Loading />}
      {filteredListingsView?.length > 0 && (
        <Grid container direction="row" spacing={4}>
          <Grid item xs={12}>
            {filteredListingsView}
          </Grid>
        </Grid>
      )}
      {filteredListingsView?.length === 0 && <span>There are no results with the selected filters.</span>}
    </div>
  );
};

export default ListingView;
