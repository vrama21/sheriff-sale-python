import React from 'react';
import ReactPaginate from 'react-paginate';
import { paginateStyles } from './Paginate.style';

const Paginate = ({ onClick, pageCount }) => {
  const classes = paginateStyles();

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
