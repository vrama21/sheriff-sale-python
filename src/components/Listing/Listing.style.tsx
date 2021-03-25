import { makeStyles } from '@material-ui/core/styles';

export const listingStyles = makeStyles((theme) => ({
  root: {
    margin: '2rem 0 0 0',
    position: 'relative',
  },
  listingContainer: {
    background: theme.palette.grey[700],
    border: `2px solid ${theme.palette.grey[500]}`,
    borderRadius: '0 0 0.5rem 0.5rem',
    boxShadow: `3px 4px ${theme.palette.grey[900]}`,
    display: 'flex',
    padding: '1rem',
    margin: '0.5rem 0',
  },
  address: {
    backgroundColor: theme.palette.grey[500],
    border: `2px solid ${theme.palette.grey[500]}`,
    borderRadius: '0.5rem 0.5rem 0 0',
    color: theme.palette.primary.main,
    fontWeight: 'bold',
    padding: '0.5rem 1rem',
    position: 'absolute',
    textShadow: '1px 1px #000000',
    top: '-34px',
    width: '100%',
  },
  subtext: {
    color: theme.palette.primary.light,
    'font-weight': 'bold',
    textShadow: '1px 1px #000000',
  },
}));
