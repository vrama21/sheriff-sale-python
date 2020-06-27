import React from "react";
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import NativeSelect from '@material-ui/core/NativeSelect';
import InputBase from '@material-ui/core/InputBase';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';


const BootstrapInput = withStyles((theme) => ({
  root: {
    'label + &': {
      marginTop: theme.spacing(3),
    },
  },
  input: {
    borderRadius: 4,
    position: 'relative',
    backgroundColor: theme.palette.background.paper,
    border: '1px solid #ced4da',
    fontSize: 16,
    padding: '10px 26px 10px 12px',
    transition: theme.transitions.create(['border-color', 'box-shadow']),
    // Use the system font instead of the default Roboto font.
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    '&:focus': {
      borderRadius: 4,
      borderColor: '#80bdff',
      boxShadow: '0 0 0 0.2rem rgba(0,123,255,.25)',
    },
  },
}))(InputBase);

const useStyles = makeStyles((theme) => ({
  margin: {
    margin: theme.spacing(1),
  },
}));

export default function SearchFilters({
  filters,
  onChange,
  onFilterChange,
  onSubmit,
  response
}) {
  const classes = useStyles();

  return (
    <div className="filter-container">
      <div className="flex justify-center mt-5">
        <form method="POST" onSubmit={onSubmit}>
          <FormControl className={classes.margin}>
            <InputLabel>County</InputLabel>
            <Select
              id="county-select"
              name="county"
              onChange={onFilterChange}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {response?.counties.map((county, i) => (
                <MenuItem
                  key={`county-${i}`}
                  value={county}
                >
                  {county}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl className={classes.margin}>
            <InputLabel>City</InputLabel>
            <Select
              id="city-select"
              name="city"
              onChange={onFilterChange}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {filters?.county
              ? Object.keys(response?.njData[filters.county].cities).map((city, i) => (
                <MenuItem
                  key={`city-${i}`}
                  value={city}
                >
                  {city}
                </MenuItem>
              ))
              : response?.cities.map((city, i) => (
                <MenuItem
                  key={`city-${i}`}
                  value={city}
                >
                  {city}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl className={classes.margin}>
            <InputLabel>Sale Date</InputLabel>
            <Select
              id="saleDate-select"
              name="saleDate"
              onChange={onFilterChange}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {response?.saleDates.map((saleDate, i) => (
                <MenuItem
                  key={`saleDate-${i}`}
                  value={saleDate}
                >
                  {saleDate}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <input
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            type="submit"
            value="Submit"
          />
          <button
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            id="filter-reset"
          >
            Reset
            </button>
        </form>
      </div>
    </div >
  );
};
