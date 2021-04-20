import { makeStyles } from '@material-ui/core';

export const listingTableStyles = makeStyles((theme) => ({
  tableContainer: {
    border: 'solid 1px blue',
    margin: '0 auto',
  },
  tableHeader: {
    background: 'aliceblue',
    color: 'black',
    fontWeight: 'bold',
  },
  tableRow: {
    padding: '10px',
    border: `solid 1px ${theme.palette.primary.main}`,
  },
}));
