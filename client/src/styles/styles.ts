import { makeStyles, Theme } from '@material-ui/core';

const useGlobalStyles = makeStyles((theme: Theme) => ({
  container: {
    display: 'flex',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    margin: '0 6rem',
    textAlign: 'center',
  },
}));

export default useGlobalStyles;