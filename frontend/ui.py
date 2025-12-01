import streamlit as st
import requests

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="DreamHome AI",
    page_icon="🏡",
    layout="centered"
)

# --- Custom CSS for "Attractive" UI ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        font-size: 18px;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.title("🏡 DreamHome AI")
st.markdown("### Intelligent Real Estate Valuation")
st.markdown("Enter the property specifications below to receive an instant AI-powered valuation.")
st.markdown("---")

# --- Main Form ---
with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("🏠 Property Details")
        sq_ft = st.number_input("Square Feet (Area)", min_value=500, max_value=10000, value=1500, step=50)
        bedrooms = st.selectbox("Number of Bedrooms", [1, 2, 3, 4, 5, 6, 7])
        bathrooms = st.selectbox("Number of Bathrooms", [1, 2, 3, 4, 5])

    with col2:
        st.subheader("📍 Location & Age")
        # CHANGED: Replaced Slider with Selectbox for a cleaner look
        loc_score = st.selectbox("Location Score (1 = Poor, 10 = Premium)", options=list(range(1, 11)), index=6)
        year = st.number_input("Year Built", min_value=1950, max_value=2024, value=2015)
        dist = st.number_input("Distance to City Center (km)", min_value=0.1, max_value=50.0, value=12.5, step=0.5)

    st.markdown("###") # Spacer
    
    # Large Predict Button
    submit_btn = st.button("✨ Predict Market Value")

# --- Results Section ---
if submit_btn:
    # Payload matching FastAPI expectation
    payload = {
        "Square_Feet": sq_ft,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Location_Score": loc_score,
        "Distance_to_City_km": dist,
        "Year_Built": year
    }

    with st.spinner("🤖 Analyzing market trends and calculating value..."):
        try:
            # Call API
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                price = result["predicted_price"]
                
                # Show result in a nice Metric card
                st.markdown("---")
                st.markdown("<h3 style='text-align: center;'>Estimated Property Value</h3>", unsafe_allow_html=True)
                
                # Using 3 columns to center the metric
                m_col1, m_col2, m_col3 = st.columns([1, 2, 1])
                with m_col2:
                    st.metric(label="", value=f"₹ {price:,.2f}", delta="AI High Confidence")
                
                st.success("✅ Valuation complete based on current market data.")
            else:
                st.error(f"⚠️ Error: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("🚨 Connection Error: Is the backend server running?")