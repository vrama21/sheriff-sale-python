// @ts-nocheck
import React from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';

const mapStyles = {
  height: '100%',
  width: '100%',
}

const ListingImage = () => {
  console.log(props)
  return (<Map
    google={{ apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY }}
    style={mapStyles}
    zoom={14}
    initialCenter={{
      lat: -1.2884,
      lng: 36.8233
    }}
  />
  );
};

export default ListingImage;
// export default GoogleApiWrapper({
//   apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
// })(ListingImage);