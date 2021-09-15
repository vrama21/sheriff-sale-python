import React from 'react';
import { Button, ButtonProps } from '@material-ui/core';

import { buttonSubmitStyles } from './ButtonSubmit.styles';

interface ButtonSubmitProps extends ButtonProps {
  name?: string;
  value: string;
}

const ButtonSubmit: React.FC<ButtonSubmitProps> = ({ name, onClick, size, variant, value }: ButtonSubmitProps) => {
  const classes = buttonSubmitStyles();

  return (
    <Button className={`${classes.root} ${classes[name]}`} color="primary" onClick={onClick} size={size || 'large'} variant={variant || 'contained'}>
      {value}
    </Button>
  );
};

export default ButtonSubmit;
