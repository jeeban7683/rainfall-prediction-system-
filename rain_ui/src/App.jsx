import React, { useState } from 'react';
import MapComponent from './components/MapComponent';
import CitySearch from './components/CitySearch';
import RainEffect from './components/RainEffect';
import WeatherCard from './components/WeatherCard';
import PredictionPopup from './components/PredictionPopup';
import { fetchWeatherData } from './services/api';
import './App.css';

function App() {
  const [targetLocation, setTargetLocation] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isWeatherLoading, setIsWeatherLoading] = useState(false);

  const handleSearch = async (cityData, rainfallData) => {
    setIsLoading(true);
    setIsWeatherLoading(true);
    // cityData: { lat, lon, name }
    setTargetLocation(cityData);
    setPredictionData(rainfallData);
    setIsLoading(false);

    // Fetch real-time weather data
    const weather = await fetchWeatherData(cityData.lat, cityData.lon);
    setWeatherData(weather);
    setIsWeatherLoading(false);
  };

  return (
    <div className="app-container">
      <RainEffect prediction={predictionData} />
      <MapComponent 
        location={targetLocation} 
        prediction={predictionData} 
      />
      <CitySearch 
        onSearch={handleSearch} 
        isLoading={isLoading}
      />
      {targetLocation && (
        <div className="weather-popup-card" style={{
          position: 'absolute',
          top: '32px',
          right: '32px',
          zIndex: 1000,
          width: '90%',
          maxWidth: '400px',
        }}>
          <PredictionPopup cityName={targetLocation.name} prediction={predictionData} />
        </div>
      )}
      {targetLocation && (
        <WeatherCard weather={weatherData} isLoading={isWeatherLoading} />
      )}
    </div>
  );
}

export default App;
