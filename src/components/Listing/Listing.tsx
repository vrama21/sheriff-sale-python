// @ts-nocheck
import React from 'react';
import { Grid } from '@material-ui/core';
import ListingMap from '../ListingMap/ListingMap';
import { listingStyles } from './Listing.style';
import { startCase } from 'lodash';
import { ListingInterface } from '../../types';

const Listing: React.FC<ListingInterface> = ({ listing }: Listing) => {
  const classes = listingStyles();

  const listingPropertiesToDisplay = ['judgment', 'sale_date'];

  return (
    <Grid item xs={12} lg={6}>
      <Grid container className={classes.root}>
        <Grid item className={classes.address} xs={12}>
          <a href={listing.maps_url} target="_blank">
            {listing.address}
          </a>
        </Grid>
      </Grid>

      <Grid className={classes.listingContainer} container>
        <Grid item xs={4}>
          <ListingMap />
        </Grid>
        <Grid item xs={4}>
          <div>
            {listingPropertiesToDisplay.map((listingKey) => (
              <div className={{ display: 'flex' }}>
                <span className={classes.subtext}>{`${startCase(listingKey)}: `}</span>
                <span>{listing[listingKey]}</span>
              </div>
            ))}
          </div>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Listing;
