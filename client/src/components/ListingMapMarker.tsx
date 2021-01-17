// @ts-ignore
import React from 'react';
import { withStyles } from '@material-ui/core'
import { Place } from '@material-ui/icons';
import { Marker } from 'react-map-gl';

const MarkerIcon = withStyles((theme) => ({
  root: {
    cursor: 'pointer',
    color: '#1978c8',
    borderRadius: '6px',
    height: '3rem',
    padding: '10px',
    width: '3rem',
  }
}))(Place);

const ListingMapMarker = ({ latitude, longitude }) => (
  <Marker
    latitude={latitude}
    longitude={longitude}
  >
    <MarkerIcon />
  </Marker>
);

export default ListingMapMarker;