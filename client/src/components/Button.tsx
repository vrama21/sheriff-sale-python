// @ts-nocheck
import { makeStyles, Theme } from '@material-ui/core';
import React, { MouseEventHandler } from 'react';

type ButtonProps = {
  onClick?: MouseEventHandler<HTMLButtonElement>
  text?: string
}

const useStyles = makeStyles((theme: Theme) => ({
  button: {
    background: theme.palette.primary.main,
    border: '1px solid black',
    borderRadius: '0.35rem',
    color: 'white',
    cursor: 'pointer',
    fontWeight: 700,
    minWidth: 100,
    padding: '0.5rem 1rem',

    '&:hover': {
      background: theme.palette.primary.dark,
    },
  },
}))

const Button = ({ onClick, text }: ButtonProps) => {
  const classes = useStyles();

  return (
    <div>
      <button
        className={classes.button}
        onClick={onClick}
        type="submit"
      >
        {text}
      </button>
    </div>
  );
}

export default Button;