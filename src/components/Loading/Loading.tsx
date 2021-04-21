import React from 'react';
import { ReactComponent as LoadingSVG } from '../../assets/loading_spinner.svg';
import { loadingStyles } from './Loading.style';

const LoadingSpinner: React.FC = () => {
  const classes = loadingStyles();

  return (
    <div className={classes.root}>
      <LoadingSVG />
    </div>
  );
};

export default LoadingSpinner;
