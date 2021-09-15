import React from 'react';
import { Grid } from '@material-ui/core';

import { formatToCurrency } from 'helpers/formatToCurrency';

import ListingMap from '../ListingMap/ListingMap';
import { listingStyles } from './Listing.style';

export interface ListingInterface {
  id: number;
  address: string;
  attorney?: string;
  attorney_phone?: string;
  city?: string;
  county: string;
  court_case?: string;
  created_on?: Date;
  deed?: string;
  deed_address?: string;
  defendant?: string;
  description?: string;
  judgment?: number;
  latitude?: string;
  longitude?: string;
  maps_url?: string;
  parcel?: string;
  plaintiff?: string;
  priors?: string;
  raw_address?: string;
  sale_date: string;
  secondary_unit?: string;
  sheriff_id?: string;
  state: string;
  status_history?: Record<string, unknown>;
  street?: string;
  unit?: string;
  unit_secondary?: string;
  upset_amount?: number;
  zip_code?: string;
}

interface ListingProps {
  listing: ListingInterface;
}

const Listing: React.FC<ListingProps> = ({ listing }: ListingProps) => {
  const classes = listingStyles();
  const formattedAddress = listing.city && listing.street && `${listing.street}, ${listing.city}, ${listing.state} ${listing.zip_code}`;

  return (
    <div className={classes.root}>
      <div className={classes.addressHeader}>{formattedAddress || listing.address}</div>

      <Grid container className={classes.listingContainer}>
        <Grid item xs={5}>
          {listing.latitude && listing.longitude && <ListingMap latitude={parseFloat(listing.latitude)} longitude={parseFloat(listing.longitude)} />}
        </Grid>
        <Grid item xs={3}>
          <div>
            <span className={classes.listingLabel}>Court Case: </span>
            <span className={classes.listingValue}>{listing.court_case}</span>
          </div>
          <div>
            <span className={classes.listingLabel}>Sale Date: </span>
            <span className={classes.listingValue}>{listing.sale_date}</span>
          </div>
          {listing.judgment && (
            <div>
              <span className={classes.listingLabel}>Judgment: </span>
              <span className={classes.listingValue}>{formatToCurrency(listing.judgment)}</span>
            </div>
          )}
          {listing.upset_amount && (
            <div>
              <span className={classes.listingLabel}>Upset Amount: </span>
              <span className={classes.listingValue}>{formatToCurrency(listing.upset_amount)}</span>
            </div>
          )}
        </Grid>
        <Grid item xs={4}>
          <div>
            <span className={classes.listingLabel}>Attorney: </span>
            <span className={classes.listingValue}>{listing.attorney}</span>
          </div>
          {listing.attorney_phone && (
            <div>
              <span className={classes.listingLabel}>Attorney Phone: </span>
              <span className={classes.listingValue}>{listing.attorney_phone}</span>
            </div>
          )}
          <div>
            <span className={classes.listingLabel}>Plaintiff: </span>
            <span className={classes.listingValue}>{listing.plaintiff}</span>
          </div>
          <div>
            <span className={classes.listingLabel}>Defendant: </span>
            <span className={classes.listingValue}>{listing.defendant}</span>
          </div>
          <div>
            {listing.priors && <span className={classes.listingLabel}>Priors: </span>}
            <span className={classes.listingValue}>{listing.priors}</span>
          </div>
        </Grid>
      </Grid>
    </div>
  );
};

export default Listing;
