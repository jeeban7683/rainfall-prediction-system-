import React from 'react';
import { Droplets, Gauge, Sun, Cloud, CloudRain, Thermometer } from 'lucide-react';
import './WeatherCard.css';

const WeatherCard = ({ weather, isLoading }) => {
  if (isLoading) {
    return (
      <div className="weather-container">
        <div className="weather-popup-card loading">
          <div className="pulse-loader"></div>
          <p style={{ margin: 0, paddingLeft: '16px', color: '#94a3b8' }}>Analyzing atmosphere...</p>
        </div>
      </div>
    );
  }

  if (!weather) return null;

  let WeatherAnimation = Cloud;
  let iconClass = 'animate-cloud';
  let weatherState = 'Cloudy / Clear';
  let theme = 'neutral';

  if (weather.weathercode >= 51 && weather.weathercode <= 99) {
    WeatherAnimation = CloudRain;
    iconClass = 'animate-rain';
    weatherState = 'Rain Showers';
    theme = 'rainy';
  } else if (weather.temperature > 28) {
    WeatherAnimation = Sun;
    iconClass = 'animate-sun';
    weatherState = 'Hot & Sunny';
    theme = 'hot';
  } else if (weather.temperature <= 15) {
    theme = 'cold';
  } else if (weather.humidity > 80) {
    theme = 'rainy';
  }

  return (
    <div className={`weather-container theme-${theme}`}>
      {/* Animated Weather State */}
      <div className="weather-popup-card delay-1 justify-center relative-overflow">
        <div className={`large-bg-icon ${iconClass}`}>
          <WeatherAnimation size={120} />
        </div>
        <div className="weather-details row-layout z-index-1">
          <span className="mwc-temp-large">{weather.temperature}°C</span>
          <span className="mwc-state-small">{weatherState}</span>
        </div>
      </div>

      {/* Grid of parameters */}
      <div className="weather-params-grid">
        <div className="weather-popup-card delay-2 param-card">
          <div className="icon-container temp-c">
            <Thermometer size={26} />
          </div>
          <span className="weather-value-large">{weather.temperature}°C</span>
          <span className="weather-label">Temperature</span>
        </div>

        <div className="weather-popup-card delay-3 param-card">
          <div className="icon-container hum-c">
            <Droplets size={26} />
          </div>
          <span className="weather-value-large">{weather.humidity}%</span>
          <span className="weather-label">Humidity</span>
        </div>

        <div className="weather-popup-card delay-4 param-card">
          <div className="icon-container pres-c">
            <Gauge size={26} />
          </div>
          <span className="weather-value-large">{weather.pressure}</span>
          <span className="weather-label">Pressure</span>
        </div>
      </div>
    </div>
  );
};

export default WeatherCard;
