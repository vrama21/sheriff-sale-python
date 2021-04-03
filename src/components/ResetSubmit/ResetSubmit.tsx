// @ts-nocheck
import React from 'react';
import { Button, withStyles } from '@material-ui/core';

const defaultStyle = { fontWeight: 'bold', margin: '0 0.5rem' };

const ResetSubmitComponent = withStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.secondary.light,
  },
}))(Button);

const ResetSubmit = ({ color, onClick, size, styleOverride, variant }) => (
  <ResetSubmitComponent
    color={color || 'secondary'}
    onClick={onClick}
    size={size || 'large'}
    style={styleOverride || defaultStyle}
    variant={variant || 'contained'}
  >
    Reset
  </ResetSubmitComponent>
);

export default ResetSubmit;
