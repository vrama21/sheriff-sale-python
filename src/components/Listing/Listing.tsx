// @ts-nocheck
import React from 'react';
import { Grid } from '@material-ui/core';
import ListingMap from '../ListingMap/ListingMap';

import { listingStyles } from './Listing.style';
import { ListingInterface } from '../../types';
import { formatToCurrency } from '../../helpers/formatToCurrency';
import googleMapsIcon from '../../assets/google-maps-icon.png';

const Listing: React.FC<ListingInterface> = ({ listing }: ListingInterface) => {
  const classes = listingStyles();

  return (
    <Grid item xs={12} lg={6}>
      <Grid container className={classes.root}>
        <Grid item className={classes.addressHeader} xs={12}>
          {listing.address}
          {listing.maps_url && (
            <a href={listing.maps_url} target="_blank">
              <img style={{ margin: '0 0 0 15px', 'max-width': '3%', 'max-height': '3%' }} src={googleMapsIcon} />
            </a>
          )}
        </Grid>
      </Grid>

      <Grid className={classes.listingContainer} container>
        <Grid item xs={4}>
          <ListingMap />
        </Grid>
        <Grid item xs={2}>
          <span className={classes.listingLabel}>Sale Date: </span>
          {listing.judgment && <span className={classes.listingLabel}>Judgment: </span>}
          {listing.upset_amount && <span className={classes.listingLabel}>Upset Amount: </span>}
        </Grid>
        <Grid item xs={2}>
          <span className={classes.listingValue}>{listing.sale_date}</span>
          {listing.judgment && <span className={classes.listingValue}>{formatToCurrency(listing.judgment)}</span>}
          {listing.upset_amount && <span className={classes.listingValue}>{formatToCurrency(listing.upset_amount)}</span>}
          <span className={classes.listingValue}>{listing.priors}</span>
        </Grid>
        <Grid item xs={2}>
          <span className={classes.listingLabel}>Attorney: </span>
          <span className={classes.listingLabel}>Attorney Phone: </span>
          <span className={classes.listingLabel}>Plaintiff: </span>
          <span className={classes.listingLabel}>Defendant: </span>
        </Grid>
        <Grid item xs={2}>
          <span className={classes.listingValue}>{listing.attorney}</span>
          <span className={classes.listingValue}>{listing.attorney_phone}</span>
          <span className={classes.listingValue}>{listing.plaintiff}</span>
          <span className={classes.listingValue}>{listing.defendant}</span>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Listing;
