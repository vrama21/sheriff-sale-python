import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

const useStyles = makeStyles({
  root: {
    padding: '.5rem',
    width: '50%',
  },
});

const Listing = ({ listings }) => {
  const classes = useStyles();

  return (
    <div className="flex flex-wrap">
      {listings && listings.length > 0
        ?
        listings.map((listing, i) => (
          <Card className={classes.root} key={`listing-${i}`}>
            <CardContent>
              {listing.addressSanitized.street}
              {listing.addressSanitized.city}
            </CardContent>
          </Card>
        ))
        : 'There are no results for this county'
      }
    </div>
  );
}
export default Listing;
