import React from 'react';
import { ReactComponent as LoadingSVG } from '../../assets/loading_spinner.svg';
import { LoadingStyles } from './Loading.style';

const LoadingSpinner: React.FC = () => {
  const classes = LoadingStyles();

  return (
    <div className={classes.root}>
      <LoadingSVG />
    </div>
  );
};

export default LoadingSpinner;
