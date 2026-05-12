# Rainfall Prediction System - Backend

Python-based machine learning backend for rainfall prediction.

## Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

## Running

```bash
python app.py
```

## Dependencies

All dependencies are listed in [requirements.txt](requirements.txt):

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **scikit-learn** - ML algorithms and preprocessing
- **xgboost** - Gradient boosting framework
- **lightgbm** - Light gradient boosting machine
- **catboost** - Categorical boosting
- **tensorflow** - Deep learning framework (LSTM)
- **requests** - HTTP library for APIs
- **streamlit** - Web app framework
- **joblib** - Model persistence

## Project Structure

```
rainfll2/
├── api/
│   ├── nasa_api.py
│   └── weather_api.py
├── features/
│   └── feature_engineering.py
├── models/
│   └── lstm_model.h5
├── prediction/
│   └── predict.py
├── training/
│   ├── train_advanced_model.py
│   ├── train_ensemble.py
│   ├── train_lstm.py
│   ├── train_ml.py
│   └── train_tuned_ensemble.py
├── data/
│   └── india_rainfall_dataset.csv
├── app.py
└── requirements.txt
```

## Key Components

### API Integration (`api/`)
- NASA API for satellite data
- Weather API for current conditions

### Feature Engineering (`features/`)
- Data preprocessing
- Feature extraction and transformation

### Models (`models/`)
- Pre-trained LSTM model
- Ensemble models (CatBoost, XGBoost, LightGBM)

### Training Scripts (`training/`)
- Individual model training
- Ensemble training
- Hyperparameter tuning

### Prediction (`prediction/`)
- Real-time prediction module
- Batch prediction capabilities

## Data

Training data: `data/india_rainfall_dataset.csv`

## Usage

1. **Training Models**: Run scripts in `training/` directory
2. **Making Predictions**: Use `prediction/predict.py`
3. **API Calls**: Configured in `api/` directory

## Environment Variables

Add to `.env`:
```
NASA_API_KEY=your_key
WEATHER_API_KEY=your_key
```

## Notes

- Python 3.8+ required
- TensorFlow requires significant disk space
- Models are pre-trained; use training scripts to retrain
- Ensure virtual environment is activated before installing packages

