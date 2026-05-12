import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Custom glowing neon marker
const glowingIcon = L.divIcon({
  className: 'custom-div-icon',
  html: "<div class='glowing-marker'></div>",
  iconSize: [20, 20],
  iconAnchor: [10, 10],
  popupAnchor: [0, -15]
});

// We can still set it as default or just use it directly in the Marker component
L.Marker.prototype.options.icon = glowingIcon;

// Component to handle smooth zooming
function ChangeView({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom, {
        duration: 2,
        easeLinearity: 0.25
      });
    }
  }, [center, zoom, map]);
  return null;
}

const MapComponent = ({ location, prediction }) => {
  const indiaCenter = [20.5937, 78.9629];
  // Zoom level 9 as requested (between 8-10)
  const zoomLevel = location ? 9 : 5;

  return (
    <MapContainer 
      center={indiaCenter} 
      zoom={5} 
      scrollWheelZoom={true}
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      
      <ChangeView center={location ? [location.lat, location.lon] : indiaCenter} zoom={zoomLevel} />

      {location && (
        <>
          {location.geojson && (
            <GeoJSON 
              key={`${location.lat}-${location.lon}`}
              data={location.geojson} 
              style={{
                color: '#fca5a5',
                weight: 1,
                opacity: 0.8,
                fillColor: '#fca5a5',
                fillOpacity: 0.05,
                className: 'glowing-boundary'
              }}
            />
          )}
          <Circle
            center={[location.lat, location.lon]}
            pathOptions={{ color: '#fca5a5', fillColor: '#fca5a5', fillOpacity: 0.05, weight: 1 }}
            radius={8000}
            className="glowing-circle"
          />
          <Marker position={[location.lat, location.lon]}>
          </Marker>
        </>
      )}
    </MapContainer>
  );
};

export default MapComponent;
