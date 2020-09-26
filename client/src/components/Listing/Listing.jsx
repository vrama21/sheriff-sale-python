import React from "react";
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  root: {
    border: '1px solid black',
    background: 'white',
    width: '50%',
  },
  subtext: {
    color: 'red',
    'font-weight': 'bold',
  }
});

export default function Listing ({ listings }) {
  const classes = useStyles();

  return (
    <div className="flex flex-wrap">
      {listings && listings.length > 0
        ? listings.map((listing, i) => (
          <div className={classes.root} key={`listing-${i}`}>
            <div>
              <span className={classes.subtext}>Address: </span>
              {listing.address_sanitized}
            </div>
            <div>
              <span className={classes.subtext}>City: </span>
              {listing.city}
            </div>
            <div><span className={classes.subtext}>County: </span>
              {listing.county}
            </div>
          </div>
        ))
        : 'There are no results'
      }
    </div>
  );
}
