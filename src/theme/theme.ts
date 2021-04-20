import { colors, unstable_createMuiStrictModeTheme as createMuiTheme } from '@material-ui/core';

export default createMuiTheme({
  palette: {
    primary: {
      main: '#3D5A80',
      dark: '#2C405B',
      contrastText: colors.common.white,
    },
    secondary: {
      light: colors.red[400],
      main: '#98C1D9',
      dark: colors.red[900],
      contrastText: colors.common.white,
    },
    success: {
      light: '#A5C8B7',
      main: '#81B29A',
      dark: '#53886E',
    },
    type: 'dark',
  },
});
