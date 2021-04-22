import React from 'react';
import { GoogleMap, Marker } from '@react-google-maps/api';

import { listingMapStyles } from './ListingMap.styles';

interface ListingMapProps {
  latitude: number;
  longitude: number;
}

const ListingMap: React.FC<ListingMapProps> = ({ latitude, longitude }: ListingMapProps) => {
  const classes = listingMapStyles();

  const containerStyle = {
    width: 400,
    height: 350,
  };

  const coordinates = {
    lat: latitude,
    lng: longitude,
  };

  return (
    <div className={classes.mapContainer}>
      <GoogleMap mapContainerStyle={containerStyle} center={coordinates} zoom={17}>
        <Marker position={coordinates}></Marker>
      </GoogleMap>
    </div>
  );
};

export default React.memo(ListingMap);
