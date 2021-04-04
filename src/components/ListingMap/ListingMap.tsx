// @ts-nocheck
import React, { useState } from 'react';
import ReactMapGL, { Marker } from 'react-map-gl';
import { makeStyles, withStyles } from '@material-ui/core';
import { Place } from '@material-ui/icons';

const initialViewport = {
  display: 'block',
  width: 350,
  height: 200,
  latitude: 39.483807,
  longitude: -74.510981,
  zoom: 15,
};

const useStyles = makeStyles(() => ({
  mapContainer: {
    marginRight: '1rem',
  },
}));

const MarkerIcon = withStyles(() => ({
  root: {
    cursor: 'pointer',
    color: '#1978c8',
    borderRadius: '6px',
    height: '3rem',
    padding: '10px',
    width: '3rem',
  },
}))(Place);

const ListingMap = () => {
  const classes = useStyles();
  const [viewPort, setViewport] = useState(initialViewport);

  return (
    <div className={classes.mapContainer}>
      <ReactMapGL {...viewPort} mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_API_KEY} onViewportChange={(viewport) => setViewport(viewport)}>
        <Marker latitude={viewPort.latitude} longitude={viewPort.longitude}>
          <MarkerIcon />
        </Marker>
      </ReactMapGL>
    </div>
  );
};

export default ListingMap;
