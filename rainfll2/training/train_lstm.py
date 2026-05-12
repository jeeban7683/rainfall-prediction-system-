import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

df = pd.read_csv('data/india_rainfall_dataset.csv')

data = df[['rain']].values

scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

X, y = [], []

window = 10

for i in range(window, len(data_scaled)):
    X.append(data_scaled[i-window:i])
    y.append(data_scaled[i])

X, y = np.array(X), np.array(y)

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=10, batch_size=16)

model.save('models/lstm_model.h5')

print("LSTM Model Trained!")