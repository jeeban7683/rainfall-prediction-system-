import React from 'react';
import { CloudRain, Sun, Cloud, CloudLightning } from 'lucide-react';

const WeatherIcon = ({ type }) => {
  switch (type?.toLowerCase()) {
    case 'heavy rain': return <CloudLightning className="weather-icon" style={{ color: '#60a5fa' }} />;
    case 'moderate rain': return <CloudRain className="weather-icon" style={{ color: '#93c5fd' }} />;
    case 'cloudy': return <Cloud className="weather-icon" style={{ color: '#94a3b8', filter: 'drop-shadow(0 0 8px rgba(148, 163, 184, 0.4))' }} />;
    default: return <Sun className="weather-icon" style={{ color: '#facc15', filter: 'drop-shadow(0 0 15px rgba(250, 204, 21, 0.6))' }} />;
  }
};

const PredictionPopup = ({ cityName, prediction }) => {
  return (
    <div style={{ 
      textAlign: 'center', 
      padding: '24px 20px', 
      minWidth: '220px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '12px'
    }}>
      <h3 style={{ 
        margin: '0', 
        color: '#f8fafc',
        fontSize: '1.4rem',
        textShadow: '0 0 10px rgba(248, 250, 252, 0.4)',
        borderBottom: '1px solid rgba(56, 189, 248, 0.3)',
        paddingBottom: '8px',
        width: '100%'
      }}>
        {cityName}
      </h3>
      {prediction ? (
        <>
          <div style={{ padding: '10px 0' }}>
            <WeatherIcon type={prediction.type} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <p style={{ 
              fontSize: '2.5rem', 
              fontWeight: '800', 
              color: '#38bdf8',
              margin: '0',
              textShadow: '0 0 15px rgba(56, 189, 248, 0.6)',
              lineHeight: '1'
            }}>
              {prediction.amount}
              <span style={{ fontSize: '1.2rem', marginLeft: '4px', color: '#94a3b8', fontWeight: '500', textShadow: 'none' }}>mm</span>
            </p>
            <p style={{ 
              color: '#bae6fd', 
              fontSize: '1rem', 
              fontWeight: '500',
              margin: '0',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              {prediction.type}
            </p>
          </div>
        </>
      ) : (
        <div style={{ padding: '20px', color: '#94a3b8' }}>
          <p className="animate-pulse">Analyzing meteorological data...</p>
        </div>
      )}
    </div>
  );
};

export default PredictionPopup;
