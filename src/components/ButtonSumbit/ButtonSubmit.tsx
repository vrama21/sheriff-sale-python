import React from 'react';
import { Button } from '@material-ui/core';

const defaultStyle = { fontWeight: 'bold', margin: '0 0.5rem' };

export const ButtonSubmit = ({ color, onClick, size, styleOverride, variant }) => (
  <Button color={color || 'primary'} onClick={onClick} size={size || 'large'} style={styleOverride || defaultStyle} variant={variant || 'contained'}>
    Submit
  </Button>
);
