import { makeStyles } from '@material-ui/core';

export const buttonSubmitStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.success.main,
    '&:hover': {
      backgroundColor: theme.palette.success.dark,
    },
  },
}));
