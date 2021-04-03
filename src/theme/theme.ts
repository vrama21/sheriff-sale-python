import { colors, unstable_createMuiStrictModeTheme as createMuiTheme } from "@material-ui/core";

export default createMuiTheme({
  palette: {
    primary: {
      light: '#81B29A',
      main: colors.green[500],
      dark: colors.green[700],
      contrastText: colors.common.white,
    },
    secondary: {
      light: colors.red[400],
      main: colors.red[600],
      dark: colors.red[900],
      contrastText: colors.common.white,
    },
    success: {
      main: "#81B29A"
    },
    type: 'dark',
  }
});
