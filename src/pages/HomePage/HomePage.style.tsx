import { makeStyles } from '@material-ui/core/styles';

export const homePageStyles = makeStyles((theme) => ({
  root: {
    textAlign: 'center',
  },
  header: {
    background: theme.palette.primary.dark,
    paddingBottom: '2rem',
  },
  title: {
    padding: '0.5rem 0',
  },
}));
