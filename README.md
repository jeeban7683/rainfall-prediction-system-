# 🌧️ AI-Powered Rainfall Prediction System

A sophisticated, high-precision rainfall forecasting system that leverages a **Hybrid Ensemble Architecture** combining Gradient Boosted Trees and Deep Learning (LSTM) to provide accurate meteorological predictions.

![Project Preview](https://img.shields.io/badge/Architecture-Hybrid_Ensemble-blue?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Python-3.x-green?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react)
![ML](https://img.shields.io/badge/Scikit--Learn-XGBoost-orange?style=for-the-badge)

---

## 🚀 Key Features

- **Hybrid Prediction Engine**: Combines 4 specialized ML models with an LSTM Neural Network.
- **Multi-Source Data Integration**: Fetches real-time weather data and correlates it with **NASA Satellite Data**.
- **Spatial Awareness**: Analyzes neighboring regions to account for atmospheric movement and spatial correlation.
- **Time-Series Analysis**: Uses historical rainfall lags (1, 3, and 7 days) for short-term trend detection.
- **Dual-Interface System**:
  - **Modern Web Dashboard**: Built with React & Vite, featuring interactive maps and dynamic rain effects.
  - **Analytical Studio**: Built with Streamlit for deep-dive meteorological analysis.

---

## 🧠 The Architecture (The "Brains")

The system uses a weighted ensemble approach to ensure maximum accuracy:

### 1. The ML Ensemble (70% weight)
We use a weighted average of four state-of-the-art algorithms:
- **XGBoost (35%)**: For handling complex non-linear relationships.
- **LightGBM (30%)**: Optimized for fast, accurate gradient boosting.
- **Random Forest (20%)**: To reduce variance and prevent overfitting.
- **CatBoost (15%)**: Specialized in handling categorical and spatial data.

### 2. The LSTM Neural Network (30% weight)
A **Long Short-Term Memory (LSTM)** network processes the last 10 days of rainfall history to capture temporal patterns that traditional ML might miss.

---

## 📂 Project Structure

```bash
├── rain_ui/              # Modern React + Vite Frontend
│   ├── src/components/   # Map, Search, and Rain Effect components
│   └── src/services/     # API integration layer
├── rainfll2/             # Backend & ML Core
│   ├── api/              # Weather & NASA API integrations
│   ├── data/             # Datasets (India Rainfall Data)
│   ├── models/           # Pre-trained .pkl and .h5 models
│   ├── prediction/       # Core prediction logic (Ensemble + LSTM)
│   ├── training/         # Model training and tuning scripts
│   └── app.py            # Streamlit Dashboard
└── README.md
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for React UI)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd rainfll2
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit Dashboard:
   ```bash
   streamlit run app.py
   ```

### Frontend Setup
1. Navigate to the UI directory:
   ```bash
   cd rain_ui
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## 🛰️ Data Sources
- **OpenWeather API**: For real-time temperature, humidity, and pressure.
- **NASA Satellite Data**: For advanced atmospheric readings.
- **Historical Dataset**: Specialized rainfall records for the Indian subcontinent.

---

## 📝 License
This project is for educational and research purposes in the field of meteorology and machine learning.