import { colors, createMuiTheme } from "@material-ui/core";

export default createMuiTheme({
  palette: {
    primary: {
      light: colors.green[300],
      main: colors.green[500],
      dark: colors.green[700],
    },
    secondary: {
      light: colors.red[400],
      main: colors.red[600],
      dark: colors.red[900],
    },
    type: 'dark',
  }
});
