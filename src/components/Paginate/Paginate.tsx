import React from 'react';
import ReactPaginate from 'react-paginate';
import { paginateStyles } from './Paginate.style';

interface PaginateProps {
  onClick: (selectedItem: { selected: number }) => void;
  pageCount: number;
}

const Paginate: React.FC<PaginateProps> = ({ onClick, pageCount }) => {
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
      marginPagesDisplayed={5}
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
