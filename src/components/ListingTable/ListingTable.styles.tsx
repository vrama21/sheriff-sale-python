import { makeStyles } from '@material-ui/core';

export const listingTableStyles = makeStyles((theme) => ({
  tableContainer: {
    border: `solid 3px ${theme.palette.primary.main}`,
    margin: '0 auto',
    maxWidth: '1200px',
    minWidth: '960px',
  },

  tableHeader: {
    background: theme.palette.secondary.main,
    color: theme.palette.primary.main,
    fontSize: '18px',
    fontWeight: 'bold',
    minWidth: '70px',
    textAlign: 'center',

    '&:last-child(2)': {
      width: '300px',
    },

    '&:last-child': {
      width: '150px',
    },
  },

  tableRow: {
    border: `solid 2px ${theme.palette.primary.main}`,
    lineHeight: 1,
    padding: '10px',
    textAlign: 'center',

    '&:nth-child(odd)': {
      background: theme.palette.primary.dark,
    },

    '&:nth-child(even)': {
      background: theme.palette.primary.main,
    },
  },

  tableCell: {
    fontSize: '1rem',
    fontWeight: 'bold',
    textAlign: 'center',
    '& a': {
      color: 'white',
    },
  },
}));
