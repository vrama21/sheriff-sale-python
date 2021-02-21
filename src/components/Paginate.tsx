import React from 'react';
import ReactPaginate from 'react-paginate';
import { makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  activeLinkStyle: {
    color: theme.palette.primary.light,
    borderBottom: '1px solid'
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
    fontWeight: "bold",
    outline: 'none',
    '&:hover': {
      color: theme.palette.primary.light,
      cursor: 'pointer'
    }
  },
}));

const Paginate = ({ onClick, pageCount }) => {
  const classes = useStyles();

  if (pageCount === 0) {
    return null;
  }

  return (
    <ReactPaginate
      previousLabel="<"
      previousLinkClassName={classes.linkStyle}
      nextLabel=">"
      nextLinkClassName={classes.linkStyle}
      breakLabel="..."
      breakClassName={classes.basicStyle}
      breakLinkClassName={classes.linkStyle}
      containerClassName={classes.containerStyle}
      initialPage={0}
      pageCount={pageCount}
      marginPagesDisplayed={3}
      nextClassName={classes.basicStyle}
      pageClassName={classes.basicStyle}
      pageLinkClassName={classes.linkStyle}
      pageRangeDisplayed={3}
      previousClassName={classes.basicStyle}
      onPageChange={onClick}
      activeLinkClassName={classes.activeLinkStyle}
    />

  );
};

export default Paginate;
