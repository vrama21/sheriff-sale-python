import { withStyles } from '@material-ui/core/styles';
import { Select } from '@material-ui/core';
import { MenuProps as MenuP } from '@material-ui/core/Menu';

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

export const FilterSelect = withStyles(() => ({
  root: {
    border: '1px solid grey',
    fontWeight: 'bold',
    paddingBottom: '1rem',
  },
}))(Select);
