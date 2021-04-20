import { makeStyles } from '@material-ui/core/styles';

export const homePageStyles = makeStyles((theme) => ({
  root: {
    textAlign: 'center',
    color: theme.palette.common.white,
  },
  header: {
    background: '#293241',
    paddingBottom: '2rem',
  },
  title: {
    padding: '0.5rem 0',
  },
}));
