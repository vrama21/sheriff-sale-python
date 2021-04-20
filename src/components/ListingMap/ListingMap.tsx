import React, { useState } from 'react';
import { GoogleMap, Marker } from '@react-google-maps/api';
import { listingMapStyles } from './ListingMap.styles';

interface ListingMapProps {
  latitude: number;
  longitude: number;
}

const ListingMap: React.FC<ListingMapProps> = ({ latitude, longitude }: ListingMapProps) => {
  const classes = listingMapStyles();

  const containerStyle = {
    width: 300,
    height: 250,
  };

  const coordinates = {
    lat: latitude,
    lng: longitude,
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [map, setMap] = useState(null);

  const onUnmount = React.useCallback(() => {
    setMap(null);
  }, []);

  return (
    <div className={classes.mapContainer}>
      <GoogleMap mapContainerStyle={containerStyle} center={coordinates} zoom={17} onUnmount={onUnmount}>
        <Marker position={coordinates}></Marker>
      </GoogleMap>
    </div>
  );
};

export default React.memo(ListingMap);
