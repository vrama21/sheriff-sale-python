import React, { useMemo } from 'react';
import { useTable } from 'react-table';
import { Link } from 'react-router-dom';
import { listingTableStyles } from './ListingTable.styles';
import { ListingInterface } from '../../types/types';
import { formatToCurrency } from '../../helpers/formatToCurrency';
import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';

interface ListingTableProps {
  listings: ListingInterface[];
}

const ListingTable: React.FC<ListingTableProps> = ({ listings }: ListingTableProps) => {
  const classes = listingTableStyles();

  const columnHeaders = [
    {
      Header: 'Address',
      accessor: 'address',
    },
    {
      Header: 'County',
      accessor: 'county',
    },
    {
      Header: 'Sale Date',
      accessor: 'saleDate',
    },
    {
      Header: 'Attorney',
      accessor: 'attorney',
    },
    {
      Header: 'Upset Amount or Judgment',
      accessor: 'upsetOrJudgment',
    },
    {
      Header: '',
      accessor: 'linkToListing',
    },
  ];

  const data = useMemo(
    () =>
      listings.map((listing) => ({
        address: listing.address,
        attorney: listing.attorney,
        county: listing.county,
        defendant: listing.defendant,
        saleDate: listing.sale_date,
        upsetOrJudgment: formatToCurrency(listing.judgment || listing.upset_amount),
        linkToListing: <Link to={`listing/${listing.id}`}>View Listing</Link>,
      })),
    [listings],
  );

  const columns = useMemo(() => columnHeaders, []);

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data });

  const tableHeaders = headerGroups.map((headerGroup) => {
    return (
      <TableRow {...headerGroup.getHeaderGroupProps()}>
        {headerGroup.headers.map((column) => (
          <TableCell className={classes.tableHeader} {...column.getHeaderProps()}>
            {column.render('Header')}
          </TableCell>
        ))}
      </TableRow>
    );
  });

  const tableRows = rows.map((row) => {
    prepareRow(row);

    return (
      <TableRow className={classes.tableRow} {...row.getRowProps()}>
        {row.cells.map((cell) => {
          return (
            <TableCell className={classes.tableCell} {...cell.getCellProps()}>
              {cell.render('Cell')}
            </TableCell>
          );
        })}
      </TableRow>
    );
  });

  return (
    <Table className={classes.tableContainer} stickyHeader={true} {...getTableProps()}>
      <TableHead>{tableHeaders}</TableHead>
      <TableBody {...getTableBodyProps()}>{tableRows}</TableBody>
    </Table>
  );
};

export default ListingTable;
