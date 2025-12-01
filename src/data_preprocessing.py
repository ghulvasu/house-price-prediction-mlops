import pandas as pd
import numpy as np
import os
import joblib  # <--- Added this to save the scaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preprocess_data():
    # --- Settings ---
    raw_data_path = "data/raw/house_prices.csv"
    processed_path = "data/processed"
    scaler_path = "models/scaler.pkl"  # <--- New path for scaler
    test_size = 0.2
    random_state = 42

    print("🚀 Starting Data Preprocessing...")

    # 1. Load Data
    df = pd.read_csv(raw_data_path)
    
    # 2. Feature Engineering
    df['House_Age'] = 2024 - df['Year_Built']
    df = df.drop(columns=['Year_Built'])

    target = 'Price_INR'
    X = df.drop(columns=[target])
    y = df[target]

    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # 4. Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. Save the Scaler (CRITICAL STEP)
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    joblib.dump(scaler, scaler_path)
    print(f"✅ Scaler saved to {scaler_path}")

    # 6. Save Processed Data
    train_data = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_data[target] = y_train.reset_index(drop=True)

    test_data = pd.DataFrame(X_test_scaled, columns=X.columns)
    test_data[target] = y_test.reset_index(drop=True)

    os.makedirs(processed_path, exist_ok=True)
    train_data.to_csv(os.path.join(processed_path, "train.csv"), index=False)
    test_data.to_csv(os.path.join(processed_path, "test.csv"), index=False)

    print(f"✅ Preprocessing complete. Files saved to {processed_path}")

if __name__ == "__main__":
    preprocess_data()