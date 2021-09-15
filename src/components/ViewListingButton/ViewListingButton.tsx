import { Link } from 'react-router-dom';

import { viewListingButtonStyles } from './ViewListingButton.styles';
import ArrowForwardIcon from '@material-ui/icons/ArrowForward';
import ButtonSubmit from '../ButtonSubmit/ButtonSubmit';

const ViewListingButton = ({ listingId }) => {
  const classes = viewListingButtonStyles();

  return (
    <>
      <Link to={`listing/${listingId}`}>
        <ButtonSubmit className={classes.viewListingButtonRoot} value="View Listing">
          <ArrowForwardIcon />
        </ButtonSubmit>
      </Link>
    </>
  );
};

export default ViewListingButton;
