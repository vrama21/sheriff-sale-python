import React from 'react';
import { Button, ButtonProps } from '@material-ui/core';

import { resetSubmitStyles } from './ResetSubmit.styles';

const ResetSubmit: React.FC<ButtonProps> = ({ className, color, onClick, size, variant }: ButtonProps) => {
  const classes = resetSubmitStyles();

  return (
    <Button
      className={classes.root || className}
      color={color || 'secondary'}
      onClick={onClick}
      size={size || 'large'}
      variant={variant || 'contained'}
    >
      Reset
    </Button>
  );
};

export default ResetSubmit;
