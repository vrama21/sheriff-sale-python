import React from "react";
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  root: {
    border: '1px solid black',
    background: theme.palette.grey[500],
    color: 'black',
    width: '50%',
  },
  subtext: {
    color: theme.palette.primary.light,
    'font-weight': 'bold',
  }
}));

export default function Listing({ listing }) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <div>
        <span className={classes.subtext}>Address: </span>
        {listing.address_sanitized}
      </div>
      <div>
        <span className={classes.subtext}>City: </span>
        {listing.city}
      </div>
      <div>
        <span className={classes.subtext}>County: </span>
        {listing.county}
      </div>
    </div >
  );
};
