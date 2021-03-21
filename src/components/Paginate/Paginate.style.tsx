import { makeStyles } from '@material-ui/core';

export const paginateStyles = makeStyles((theme) => ({
  activeLinkStyle: {
    color: theme.palette.primary.light,
    borderBottom: '1px solid',
  },
  basicStyle: { display: 'block', padding: '0.5rem' },
  containerStyle: {
    backgroundColor: theme.palette.grey[700],
    border: `2px solid ${theme.palette.grey[500]}`,
    borderRadius: '0.5rem',
    boxShadow: `3px 4px ${theme.palette.grey[900]}`,
    display: 'flex',
    justifyContent: 'center',
    margin: '2rem auto',
    padding: '0 1rem',
    width: 'fit-content',
  },
  linkStyle: {
    fontWeight: 'bold',
    outline: 'none',
    '&:hover': {
      color: theme.palette.primary.light,
      cursor: 'pointer',
    },
  },
}));
