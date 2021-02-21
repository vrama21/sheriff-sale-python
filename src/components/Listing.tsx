// @ts-nocheck
import React from "react";
import { Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ListingMap from "./ListingMap";
import { startCase } from 'lodash';

const useStyles = makeStyles((theme) => ({
  root: {
    margin: '2rem 0 0 0',
    position: 'relative',
  },
  listingContainer: {
    background: theme.palette.grey[700],
    border: `2px solid ${theme.palette.grey[500]}`,
    borderRadius: '0 0.5rem 0.5rem 0.5rem',
    boxShadow: `3px 4px ${theme.palette.grey[900]}`,
    display: 'flex',
    padding: '1rem',
    margin: '0.5rem 0',
  },
  address: {
    backgroundColor: theme.palette.grey[500],
    border: `2px solid ${theme.palette.grey[500]}`,
    borderRadius: '0.5rem 0.5rem 0 0',
    fontWeight: 'bold',
    padding: '0.5rem 1rem',
    position: 'absolute',
    top: '-34px',
    width: '100%',
  },
  subtextContainer: {
    width: '25%',
    margin: '0 1rem',
    textAlign: 'left',
  },
  subtextGroup: {
    // textAlign: 'left',
  },
  subtext: {
    color: theme.palette.primary.light,
    'font-weight': 'bold',
    textShadow: '1px 1px #000000',
  },
}));


const Listing = ({ listing }) => {
  const classes = useStyles();

  const keysToRender = ['sale_date', 'sheriff', 'court_case', 'judgment'];

  const updatedListing = {}
  keysToRender.forEach((key) => updatedListing[key] = listing[key])
  const listingEntries = Object.entries(updatedListing);
  // listingEntries[0] = Category
  // listingEntries[1] = Value

  return (
    <Grid item xs={12} lg={6}>

      <Grid container className={classes.root}>
        <Grid className={classes.address} item xs={12} sm={6}>
          {`${listing.address_sanitized} ${listing.city} ${listing.zip_code}`}
        </Grid>
      </Grid>

      <Grid className={classes.listingContainer} container>
        <Grid item xs={4}>
          <ListingMap />
        </Grid>
        <div className={classes.subtextContainer}>
          {listingEntries.map((listingEntry, listingEntryIndex) => (
            <Grid container key={`${listing.sheriff}-${listingEntryIndex}-subtext`}>
              <Grid className={classes.subtext} item xs={6}>{`${startCase(listingEntry[0])}: `}</Grid>
              <Grid item xs={6}>{listingEntry[1]}</Grid>
            </Grid>
          ))}
        </div>
      </Grid>

    </Grid >
  );
};

export default Listing;