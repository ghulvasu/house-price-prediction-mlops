import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def evaluate_model():
    # --- Settings ---
    test_data_path = "data/processed/test.csv"
    model_path = "models/model.pkl"
    metrics_path = "metrics.json"
    target = 'Price_INR'

    print("🚀 Starting Model Evaluation...")

    # 1. Load Test Data
    if not os.path.exists(test_data_path):
        raise FileNotFoundError(f"Test data not found at {test_data_path}. Run preprocessing first.")
    
    df = pd.read_csv(test_data_path)
    X_test = df.drop(columns=[target])
    y_test = df[target]

    # 2. Load the Saved Model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Run training first.")

    model = joblib.load(model_path)
    print(f"   Model loaded: {type(model).__name__}")

    # 3. Generate Predictions
    predictions = model.predict(X_test)

    # 4. Calculate Metrics
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\n📊 Evaluation Results:")
    print(f"   👉 RMSE (Root Mean Squared Error): {rmse:.2f}")
    print(f"   👉 MAE  (Mean Absolute Error):     {mae:.2f}")
    print(f"   👉 R2 Score (Accuracy):            {r2:.4f}")

    # 5. Save Metrics to JSON (Crucial for DVC/MLflow tracking)
    metrics_data = {
        "rmse": rmse,
        "mae": mae,
        "r2_score": r2
    }

    with open(metrics_path, 'w') as f:
        json.dump(metrics_data, f, indent=4)

    print(f"\n✅ Metrics saved to '{metrics_path}'")

if __name__ == "__main__":
    evaluate_model()