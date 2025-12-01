import pandas as pd
import numpy as np
import os

def generate_data():
    # Set seed for reproducibility
    np.random.seed(42)
    n_rows = 2000

    # --- Feature Generation ---
    
    # Feature 1: Square Feet (Numerical)
    # Range: 600 sqft to 4000 sqft
    square_feet = np.random.randint(600, 4000, n_rows)

    # Feature 2: Number of Bedrooms (Categorical/Ordinal)
    # Range: 1 BHK to 5 BHK
    bedrooms = np.random.randint(1, 6, n_rows)

    # Feature 3: Number of Bathrooms (Categorical/Ordinal)
    # Logic: Usually similar to bedrooms, maybe +/- 1
    bathrooms = np.random.randint(1, 5, n_rows)

    # Feature 4: Year Built (Numerical)
    # Range: 1990 to 2024
    year_built = np.random.randint(1990, 2025, n_rows)

    # Feature 5: Location Score (Ordinal)
    # 1 (Poor) to 10 (Premium Area)
    location_score = np.random.randint(1, 11, n_rows)

    # Feature 6: Distance to City Center (Numerical - Float)
    # Range: 1 km to 25 km
    distance_km = np.round(np.random.uniform(1.0, 25.0, n_rows), 2)

    # --- Target Generation: Price (in INR) ---
    
    # Base calculation (Logic: Price depends on features)
    # Assume base rate is 3000 INR per sqft
    # Premium location adds value
    # Distance reduces value
    
    base_price = (square_feet * 4500) + \
                 (bedrooms * 300000) + \
                 (bathrooms * 150000) + \
                 (location_score * 500000) - \
                 (distance_km * 50000) + \
                 (year_built * 1000) # Newer houses cost slightly more

    # Add Random Noise (to make it realistic and not a perfect equation)
    # Noise range: +/- 10% variation
    noise = np.random.normal(0, 500000, n_rows)
    final_price = base_price + noise

    # Ensure no negative prices (sanity check)
    final_price = np.where(final_price < 1500000, 1500000, final_price)

    # Create DataFrame
    df = pd.DataFrame({
        'Square_Feet': square_feet,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Year_Built': year_built,
        'Location_Score': location_score,
        'Distance_to_City_km': distance_km,
        'Price_INR': np.round(final_price, 2)
    })

    # --- Saving Data ---
    
    # Define path
    raw_data_path = os.path.join("data", "raw")
    os.makedirs(raw_data_path, exist_ok=True)
    
    file_path = os.path.join(raw_data_path, "house_prices.csv")
    
    # Save to CSV
    df.to_csv(file_path, index=False)
    print(f"✅ Success! Data generated with {n_rows} rows and saved to {file_path}")
    print(df.head())

if __name__ == "__main__":
    generate_data()