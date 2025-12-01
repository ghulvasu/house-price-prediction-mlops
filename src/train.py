import pandas as pd
import joblib
import os
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score

# --- MLflow & MinIO Configuration ---
# We set these environment variables so MLflow knows how to talk to MinIO
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"

def train_best_model():
    # --- Settings ---
    train_data_path = "data/processed/train.csv"
    model_path = "models/model.pkl"
    target = 'Price_INR'
    
    # Connect to local MLflow Server
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("House_Price_Prediction")

    print("🚀 Starting Model Training with MLflow Tracking...")

    # 1. Load Data
    df = pd.read_csv(train_data_path)
    X = df.drop(columns=[target])
    y = df[target]

    # 2. Define the Candidates
    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=50, random_state=42),
        "GradientBoosting": GradientBoostingRegressor(random_state=42)
    }

    best_model_name = None
    best_model_obj = None
    best_score = -np.inf 

    # 3. The Tournament
    print("\n📊 Comparing Models...")
    for name, model in models.items():
        scores = cross_val_score(model, X, y, cv=5, scoring='r2')
        avg_score = scores.mean()
        print(f"   👉 {name}: R2 Score = {avg_score:.4f}")

        if avg_score > best_score:
            best_score = avg_score
            best_model_name = name
            best_model_obj = model

    print(f"\n🏆 The Winner is: {best_model_name} (Score: {best_score:.4f})")

    # 4. Train the Winner
    best_model_obj.fit(X, y)

    # 5. Save Locally (For DVC Pipeline)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(best_model_obj, model_path)
    print(f"✅ Model saved locally to {model_path}")

    # 6. Log to MLflow & MinIO
    print("   📡 Logging to MLflow...")
    
    # ------------------ CHANGED LINE ------------------
    # We add 'run_name' so it shows up clearly in the UI
    run_name = f"Train_{best_model_name}"
    with mlflow.start_run(run_name=run_name):
    # --------------------------------------------------

        # Log Hyperparameters
        mlflow.log_param("best_model_name", best_model_name)
        
        # Log Metrics
        mlflow.log_metric("r2_score", best_score)
        
        # Log Model
        mlflow.sklearn.log_model(best_model_obj, "model", registered_model_name="HousePriceModel")
        
    print("✅ Experiment logged to MLflow & Artifacts uploaded to MinIO.")

if __name__ == "__main__":
    train_best_model()