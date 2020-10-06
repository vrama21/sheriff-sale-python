import React from "react";
import { Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import * as types from '../types/types';

const useStyles = makeStyles((theme) => ({
  root: {
    background: theme.palette.grey[700],
    border: `2px solid ${theme.palette.grey[500]}`,
    borderRadius: '0.5rem',
    boxShadow: `3px 4px ${theme.palette.grey[900]}`,
    padding: '0.5rem 0',
    margin: '0.5rem 0',
  },
  subtext: {
    color: theme.palette.primary.light,
    'font-weight': 'bold',
    textShadow: '1px 1px #000000',
  },
}));

export default function Listing({ listing }: { listing: types.Listing }) {
  const classes = useStyles();

  return (
    <Grid className={classes.root} container>
      <Grid item xs={4}>
        <span className={classes.subtext}>Address: </span>
      </Grid>
      <Grid item xs={8}>
        <span>{listing.address_sanitized}</span>
      </Grid>
      <Grid item xs={4}>
        <span className={classes.subtext}>City: </span>
      </Grid>
      <Grid item xs={8}>
        <span>{listing.city}</span>
      </Grid>
      <Grid item xs={4}>
        <span className={classes.subtext}>Sale Date: </span>
      </Grid>
      <Grid item xs={8}>
        <span>{listing.sale_date}</span>
      </Grid>
    </Grid >
  );
};
