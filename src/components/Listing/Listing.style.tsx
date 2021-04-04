import { makeStyles } from '@material-ui/core/styles';

export const listingStyles = makeStyles((theme) => ({
  root: {
    margin: '2rem 0 0 0',
    position: 'relative',
  },
  listingContainer: {
    background: '#3D405B',
    border: '5px solid',
    borderColor: theme.palette.primary.main,
    borderRadius: '0 0 0.5rem 0.5rem',
    display: 'flex',
    padding: '1rem',
    margin: '0.5rem 0',
  },
  addressHeader: {
    background: theme.palette.secondary.main,
    border: '5px solid',
    borderColor: theme.palette.primary.main,
    borderRadius: '0.5rem 0.5rem 0 0',
    color: theme.palette.primary.main,
    fontSize: '22px',
    fontWeight: 'bold',
    padding: '0.5rem 1rem',
    position: 'absolute',
    top: '-40px',
    width: '100%',
  },
  googleMapsLogo: {
    margin: '0 0 0 15px',
    maxHeight: '3%',
    maxWidth: '2%',
  },
  listingLabel: {
    color: theme.palette.secondary.main,
    display: 'block',
    fontWeight: 'bold',
    marginRight: '10px',
    paddingBottom: '5px',
    textAlign: 'right',
    textShadow: '1px 1px #000000',
  },
  listingValue: {
    display: 'block',
    paddingBottom: '5px',
    textAlign: 'left',
    flexWrap: 'wrap'
  },
}));
