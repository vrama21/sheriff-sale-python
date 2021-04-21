import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Listing from '../../components/Listing/Listing';
import { AppContext } from '../../App';
import { getListing } from '../../actions/actions';
import { URLParams } from '../../types/types';

const ListingPage = () => {
  const { state, dispatch } = useContext(AppContext);
  const { listingId }: URLParams = useParams();

  const listingRetrieved = state.getListingSucceeded === true;
  const listing = state.data.listing;

  useEffect(() => {
    if (!listingRetrieved) {
      getListing({ listingId, dispatch });
    }
  }, [dispatch, getListing, listingId, listingRetrieved]);

  return <div>{listing && <Listing listing={listing} />}</div>;
};

export default ListingPage;
