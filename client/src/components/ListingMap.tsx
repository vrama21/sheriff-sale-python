// @ts-nocheck
import React, { useState } from 'react';
import ReactMapGL from 'react-map-gl';
import ListingMapMarker from './ListingMapMarker';
import { makeStyles } from '@material-ui/core';

const initialViewport = {
  width: '100%',
  height: 200,
  latitude: 39.483807,
  longitude: -74.510981,
  zoom: 15,
};

const useStyles = makeStyles(() => ({
  mapContainer: {
    marginRight: '1rem'
  },
}))

const ListingMap = () => {
  const classes = useStyles();
  const [viewPort, setViewport] = useState(initialViewport);

  return (
    <div className={classes.mapContainer}>
      <ReactMapGL
        {...viewPort}
        mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_API_KEY}
        onViewportChange={(viewport) => setViewport(viewport)}
      >
        <ListingMapMarker latitude={viewPort.latitude} longitude={viewPort.longitude} />
      </ReactMapGL >
    </div>
  );
}

export default ListingMap;