import { makeStyles, Theme } from '@material-ui/core';

const useGlobalStyles = makeStyles((theme: Theme) => ({
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    margin: '1rem 3rem',
    textAlign: 'center',
  },
}));

export default useGlobalStyles;