import { Select, MenuProps as MenuP } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

export const MenuProps: Partial<MenuP> = {
  anchorOrigin: {
    vertical: 'bottom',
    horizontal: 'left',
  },
  transformOrigin: {
    vertical: 'top',
    horizontal: 'left',
  },
  getContentAnchorEl: null,
};

const FilterSelect = withStyles(() => ({
  root: {
    border: '1px solid grey',
    fontWeight: 'bold',
    paddingBottom: '1rem',
  },
}))(Select);

export default FilterSelect;
