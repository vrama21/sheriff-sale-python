import React, { useState } from 'react';
import ReactMapGL, { Marker } from 'react-map-gl';
import { makeStyles, withStyles } from '@material-ui/core';
import { Place } from '@material-ui/icons';

const useStyles = makeStyles(() => ({
  mapContainer: {
    marginRight: '1rem',
  },
}));

const MarkerIcon = withStyles(() => ({
  root: {
    cursor: 'pointer',
    color: '#1978c8',
    stroke: 'none',
  },
}))(Place);

interface ListingMapProps {
  latitude: number;
  longitude: number;
}

const ListingMap: React.FC<ListingMapProps> = ({ latitude, longitude }: ListingMapProps) => {
  const initialViewport = {
    display: 'block',
    width: 300,
    height: 250,
    latitude,
    longitude,
    zoom: 15,
  };

  const classes = useStyles();
  const markerIconSize = 20;
  const [viewPort, setViewport] = useState(initialViewport);

  return (
    <div className={classes.mapContainer}>
      <ReactMapGL {...viewPort} mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_API_KEY} onViewportChange={(viewport) => setViewport(viewport)}>
        <Marker latitude={latitude} longitude={longitude}>
          <MarkerIcon style={{ transform: `translate(${-markerIconSize / 2}px,${-markerIconSize}px)` }} />
        </Marker>
      </ReactMapGL>
    </div>
  );
};

export default ListingMap;
