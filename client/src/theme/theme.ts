import { colors, createMuiTheme } from "@material-ui/core";

export default createMuiTheme({
  palette: {
    primary: {
      light: colors.deepOrange[300],
      main: colors.deepOrange[500],
      dark: colors.deepOrange[700],
    },
    type: 'dark',
  }
});
