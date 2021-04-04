import { makeStyles } from '@material-ui/core/styles';

export const homePageStyles = makeStyles((theme) => ({
  root: {
    background: '#293241',
    padding: '1rem 0',
    textAlign: 'center',
    color: theme.palette.common.white
  },
  title: {
    padding: '0.5rem 0'
  }
}));
