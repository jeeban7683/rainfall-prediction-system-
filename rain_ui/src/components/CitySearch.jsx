import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, Wind } from 'lucide-react';
import { geocodeCity, fetchRainfallPrediction, fetchCitySuggestions } from '../services/api';

const CitySearch = ({ onSearch, isLoading: parentLoading }) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const debounceTimeout = useRef(null);

  useEffect(() => {
    if (!query.trim()) {
      setSuggestions([]);
      setIsDropdownOpen(false);
      return;
    }

    // Only run if the user is typing (dropdown is meant to be open)
    // We check if query length > 2
    if (query.length < 2) return;

    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);

    debounceTimeout.current = setTimeout(async () => {
      const results = await fetchCitySuggestions(query);
      setSuggestions(results);
      if (results.length > 0) {
        setIsDropdownOpen(true);
      }
    }, 400); // 400ms debounce

    return () => clearTimeout(debounceTimeout.current);
  }, [query]);

  const handleSelectSuggestion = async (suggestion) => {
    setQuery(suggestion.name);
    setIsDropdownOpen(false);
    await triggerSearch(suggestion.name);
  };

  const triggerSearch = async (searchQuery) => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    setError(null);
    setIsDropdownOpen(false);

    try {
      const cityData = await geocodeCity(searchQuery);
      const prediction = await fetchRainfallPrediction(cityData.lat, cityData.lon);
      onSearch(cityData, prediction);
    } catch (err) {
      setError('Could not find city or fetch data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    triggerSearch(query);
  };

  return (
    <div className="search-panel-container" style={{
      position: 'absolute',
      top: '32px',
      left: '32px',
      zIndex: 1000,
      width: '90%',
      maxWidth: '400px'
    }}>
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h2 style={{ marginBottom: '8px', fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Wind className="text-accent" style={{ color: '#38bdf8' }} /> RainCast
        </h2>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '20px' }}>
          India Rainfall Prediction Dashboard
        </p>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px', position: 'relative' }}>
          <div style={{ position: 'relative' }}>
            <MapPin size={18} style={{ 
              position: 'absolute', 
              left: '12px', 
              top: '50%', 
              transform: 'translateY(-50%)',
              color: '#94a3b8'
            }} />
            <input
              type="text"
              placeholder="Enter city or state name..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => { if (suggestions.length > 0) setIsDropdownOpen(true); }}
              onBlur={() => setTimeout(() => setIsDropdownOpen(false), 200)} // delay to allow click
              style={{
                width: '100%',
                padding: '12px 12px 12px 40px',
                borderRadius: '8px',
                border: '1px solid var(--border-glass)',
                background: 'rgba(0,0,0,0.4)',
                color: '#fff',
                fontSize: '1rem',
                outline: 'none',
                boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.5)',
                transition: 'border-color 0.3s, box-shadow 0.3s'
              }}
              onFocusCapture={(e) => {
                e.target.style.borderColor = 'var(--accent-color)';
                e.target.style.boxShadow = '0 0 8px rgba(56, 189, 248, 0.5), inset 0 2px 4px rgba(0,0,0,0.5)';
              }}
              onBlurCapture={(e) => {
                e.target.style.borderColor = 'var(--border-glass)';
                e.target.style.boxShadow = 'inset 0 2px 4px rgba(0,0,0,0.5)';
              }}
            />
            {isDropdownOpen && suggestions.length > 0 && (
              <div className="glass-panel suggestions-dropdown" style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                right: 0,
                marginTop: '8px',
                padding: '8px 0',
                maxHeight: '200px',
                overflowY: 'auto',
                zIndex: 1001,
                background: 'rgba(15, 23, 42, 0.95)'
              }}>
                {suggestions.map((item, idx) => (
                  <div 
                    key={idx}
                    className="suggestion-item"
                    style={{
                      padding: '10px 16px',
                      cursor: 'pointer',
                      borderBottom: idx < suggestions.length - 1 ? '1px solid var(--border-glass)' : 'none',
                      color: '#e2e8f0',
                      transition: 'background 0.2s',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px'
                    }}
                    onClick={() => handleSelectSuggestion(item)}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(56, 189, 248, 0.1)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    <MapPin size={14} color="#38bdf8" />
                    <span>{item.name}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <button 
            type="submit" 
            className="btn-primary" 
            disabled={loading || parentLoading}
            style={{ width: '100%', justifyContent: 'center' }}
          >
            {loading || parentLoading ? (
              'Processing...'
            ) : (
              <>
                <Search size={18} /> Predict Rainfall
              </>
            )}
          </button>
        </form>

        {error && (
          <p style={{ color: '#ef4444', fontSize: '0.8rem', marginTop: '12px' }}>{error}</p>
        )}

        <div style={{ marginTop: '24px', borderTop: '1px solid var(--border-glass)', paddingTop: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Popular Locations</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
             {['Mumbai', 'Delhi', 'Cherrapunji'].map(city => (
               <span 
                key={city} 
                className="glass-panel" 
                style={{ 
                  padding: '6px 12px', 
                  fontSize: '0.8rem', 
                  cursor: 'pointer',
                  borderColor: 'rgba(56, 189, 248, 0.3)',
                  color: '#38bdf8',
                  background: 'rgba(56, 189, 248, 0.05)',
                  transition: 'all 0.3s ease'
                }}
                onClick={() => { setQuery(city); triggerSearch(city); }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(56, 189, 248, 0.2)';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(56, 189, 248, 0.05)';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
               >
                 {city}
               </span>
             ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CitySearch;
