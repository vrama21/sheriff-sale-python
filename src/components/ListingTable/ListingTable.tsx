import React, { useMemo } from 'react';
import { useTable } from 'react-table';
import { listingTableStyles } from './ListingTable.styles';
import { ListingInterface } from '../../types/types';
import { formatToCurrency } from '../../helpers/formatToCurrency';

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
      Header: 'Sale Date',
      accessor: 'saleDate',
    },
    {
      Header: 'Attorney',
      accessor: 'attorney',
    },
    {
      Header: 'Defendant',
      accessor: 'defendant',
    },
    {
      Header: 'Upset Amount or Judgment',
      accessor: 'upsetOrJudgment',
    },
  ];

  const data = useMemo(
    () =>
      listings.map((listing) => ({
        address: listing.address,
        attorney: listing.attorney,
        defendant: listing.defendant,
        saleDate: listing.sale_date,
        upsetOrJudgment: formatToCurrency(listing.judgment || listing.upset_amount),
      })),
    [],
  );

  const columns = useMemo(() => columnHeaders, []);

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data });

  const tableHeaders = headerGroups.map((headerGroup) => {
    return (
      <tr {...headerGroup.getHeaderGroupProps()}>
        {headerGroup.headers.map((column) => (
          <th {...column.getHeaderProps()} className={classes.tableHeader}>
            {column.render('Header')}
          </th>
        ))}
      </tr>
    );
  });

  const tableRows = rows.map((row) => {
    prepareRow(row);

    return (
      <tr {...row.getRowProps()}>
        {row.cells.map((cell) => {
          return (
            <td {...cell.getCellProps()} className={classes.tableRow}>
              {cell.render('Cell')}
            </td>
          );
        })}
      </tr>
    );
  });

  return (
    <table className={classes.tableContainer} {...getTableProps()}>
      <thead>{tableHeaders}</thead>
      <tbody {...getTableBodyProps()}>{tableRows}</tbody>
    </table>
  );
};

export default ListingTable;
