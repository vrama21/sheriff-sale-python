import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';

const useStyles = makeStyles({
  root: {
    padding: '.5rem',
    width: '50%',
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

const Listing = ({ listings }) => {
  console.log(listings);
  const classes = useStyles();

  return (
    <div className="flex flex-wrap">
      {listings &&
        listings.map((listing, i) => (
          <Card className={classes.root} key={`listing-${i}`}>
            <CardContent>
              {listing.address.street}
              {listing.address.city}
            </CardContent>
          </Card>
        ))}
    </div>
  );
}
export default Listing;
