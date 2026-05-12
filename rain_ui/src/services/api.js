import axios from 'axios';

/**
 * Geocode city name to lat/lon using Nominatim API (OpenStreetMap)
 */
export const geocodeCity = async (cityName) => {
  try {
    const response = await axios.get('https://nominatim.openstreetmap.org/search', {
      params: {
        q: cityName,
        format: 'json',
        limit: 15, // Increase limit to find more potential boundaries
        countrycodes: 'in',
        polygon_geojson: 1,
        addressdetails: 1
      }
    });

    if (response.data && response.data.length > 0) {
      console.log(`Geocoding results for "${cityName}":`, response.data.map(r => ({
        type: r.geojson?.type,
        class: r.class,
        typeLabel: r.type,
        name: r.display_name
      })));

      // Priority 1: Administrative boundaries that are Polygons
      let boundaryResult = response.data.find(res => 
        res.class === 'boundary' && 
        res.type === 'administrative' && 
        res.geojson && (res.geojson.type === 'Polygon' || res.geojson.type === 'MultiPolygon')
      );

      // Priority 2: Any Polygon/MultiPolygon
      if (!boundaryResult) {
        boundaryResult = response.data.find(res => 
          res.geojson && (res.geojson.type === 'Polygon' || res.geojson.type === 'MultiPolygon')
        );
      }

      // Fallback: First result
      const result = boundaryResult || response.data[0];
      
      console.log(`Selected result for "${cityName}":`, result.display_name, 'Type:', result.geojson?.type);

      return {
        lat: parseFloat(result.lat),
        lon: parseFloat(result.lon),
        name: result.display_name.split(',')[0],
        geojson: result.geojson
      };
    }
    throw new Error('City not found');
  } catch (error) {
    console.error('Geocoding error:', error);
    throw error;
  }
};

/**
 * Fetch auto-suggestions for cities
 */
export const fetchCitySuggestions = async (query) => {
  if (!query) return [];
  try {
    const response = await axios.get('', {
      params: {
        q: query,
        format: 'json',
        limit: 5,
        countrycodes: 'in'
      }
    });
    
    // Deduplicate by name roughly
    const uniqueNames = new Set();
    const suggestions = [];
    
    for (const item of response.data) {
      // Clean up display name: usually format is "City, State, Country"
      const parts = item.display_name.split(',');
      const shortName = parts.slice(0, 2).join(',').trim();
      
      if (!uniqueNames.has(shortName)) {
        uniqueNames.add(shortName);
        suggestions.push({
          name: shortName,
          fullName: item.display_name,
          lat: parseFloat(item.lat),
          lon: parseFloat(item.lon)
        });
      }
    }
    return suggestions;
  } catch (error) {
    console.error('Suggestion error:', error);
    return [];
  }
};

/**
 * Fetch rainfall prediction.
 * Currently uses a mock/simulated response based on coordinates.
 * Replace with real backend URL when available.
 */
export const fetchRainfallPrediction = async (lat, lon) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800));

  // For demonstration, generate semi-random realistic rainfall data
  const amount = (Math.random() * 50).toFixed(1);
  let type = 'Cloudy';
  if (amount > 30) type = 'Heavy Rain';
  else if (amount > 10) type = 'Moderate Rain';
  else if (amount > 0) type = 'Light Rain';

  return {
    amount,
    type,
    timestamp: new Date().toISOString()
  };
};

/**
 * Fetch current weather data from Open-Meteo API.
 */
export const fetchWeatherData = async (lat, lon) => {
  try {
    const response = await axios.get('https://api.open-meteo.com/v1/forecast', {
      params: {
        latitude: lat,
        longitude: lon,
        current: 'temperature_2m,relative_humidity_2m,surface_pressure,weathercode'
      }
    });

    if (response.data && response.data.current) {
      return {
        temperature: response.data.current.temperature_2m,
        humidity: response.data.current.relative_humidity_2m,
        pressure: response.data.current.surface_pressure,
        weathercode: response.data.current.weathercode
      };
    }
    return null;
  } catch (error) {
    console.error('Weather fetching error:', error);
    return null;
  }
};
