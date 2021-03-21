// @ts-nocheck
import React from 'react';
import { Grid } from '@material-ui/core';
import ListingMap from '../ListingMap/ListingMap';
import { listingStyles } from './Listing.style';
import { startCase } from 'lodash'

const Listing = ({ listing }) => {
  const classes = listingStyles();

  const listingPropertiesToDisplay = ['judgment', 'sale_date'];

  return (
    <Grid item xs={12} lg={6}>
      <Grid container className={classes.root}>
        <Grid className={classes.address} item xs={12}>
          {listing.address}
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
