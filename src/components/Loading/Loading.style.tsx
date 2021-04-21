import { makeStyles } from '@material-ui/core/styles';

export const loadingStyles = makeStyles(() => ({
  root: {
    '& svg': {
      background: 'transparent',
    },
  },
}));
