// @ts-nocheck
import React from 'react';
import { Button, withStyles } from '@material-ui/core';

const defaultStyle = { fontWeight: 'bold', margin: '0 0.5rem' };

const ButtonSubmitComponent = withStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.success.main,
    '&:hover': {
      backgroundColor: theme.palette.success.dark,
    },
  },
}))(Button);

const ButtonSubmit = ({ onClick, size, styleOverride, variant }) => (
  <ButtonSubmitComponent
    color="primary"
    onClick={onClick}
    size={size || 'large'}
    style={styleOverride || defaultStyle}
    variant={variant || 'contained'}
  >
    Submit
  </ButtonSubmitComponent>
);

export default ButtonSubmit;
