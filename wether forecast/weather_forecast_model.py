import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Load data
def load_data(file_path='weather_data.csv'):
    df = pd.read_csv(file_path, parse_dates=['date'])
    df.set_index('date', inplace=True)
    df.ffill(inplace=True)  # Forward fill missing values
    return df

# Preprocess data
def preprocess_data(df):
    # Feature engineering
    df['target_temp'] = df['temperature'].shift(-1)
    df['temp_lag1'] = df['temperature'].shift(1)
    df['humidity_lag1'] = df['humidity'].shift(1)
    df.dropna(inplace=True)
    
    # Split features and target
    X = df[['temperature', 'humidity', 'wind_speed', 'pressure', 'temp_lag1', 'humidity_lag1']]
    y = df['target_temp']
    return X, y

# Train Random Forest model
def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Main workflow
if __name__ == "__main__":
    # Load and preprocess data
    df = load_data()
    print("Data after loading:")
    print(df.head())
    print(df.shape)

    X, y = preprocess_data(df)
    print("\nData after preprocessing:")
    print(X.head())
    print(y.head())
    print(X.shape, y.shape)

    # Split into train/test
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    print("\nTrain/test split shapes:")
    print(X_train.shape, X_test.shape)

    # Train and evaluate Random Forest model
    if X_train.shape[0] > 0:  # Ensure there are samples in the training set
        rf_model = train_random_forest(X_train, y_train)
        rf_pred = rf_model.predict(X_test)
        print(f"MAE: {mean_absolute_error(y_test, rf_pred)}")
    else:
        print("Error: No samples in the training set.")