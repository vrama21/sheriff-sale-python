import { colors, unstable_createMuiStrictModeTheme as createMuiTheme } from '@material-ui/core';

export default createMuiTheme({
  palette: {
    primary: {
      light: '#6487B4',
      main: '#3D5A80',
      dark: '#2C405B',
      contrastText: colors.common.white,
    },
    secondary: {
      light: '#B5D2E3',
      main: '#98C1D9',
      dark: '#4A92BC',
      contrastText: colors.common.white,
    },
    success: {
      light: '#A5C8B7',
      main: '#81B29A',
      dark: '#53886E',
    },
    warning: {
      light: '#E9A28E',
      main: '#E07A5F',
      dark: '#C14725',
    },
    type: 'dark',
  },
});
