import React from 'react';
import { Button, ButtonProps } from '@material-ui/core';
import { buttonSubmitStyles } from './ButtonSubmit.styles';

const ButtonSubmit: React.FC<ButtonProps> = ({ className, onClick, size, variant }: ButtonProps) => {
  const classes = buttonSubmitStyles();

  return (
    <Button className={className || classes.root} color="primary" onClick={onClick} size={size || 'large'} variant={variant || 'contained'}>
      Submit
    </Button>
  );
};

export default ButtonSubmit;
