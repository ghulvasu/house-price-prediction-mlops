document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = document.getElementById('btn-predict');
    const resultBox = document.getElementById('result');
    const priceDisplay = document.getElementById('price-display');

    // 1. Show Loading State
    const originalText = btn.innerText;
    btn.innerText = "⏳ Calculating...";
    btn.disabled = true;
    resultBox.classList.add('hidden');

    // 2. Gather Data
    const formData = {
        Square_Feet: parseInt(document.getElementById('sqft').value),
        Bedrooms: parseInt(document.getElementById('bedrooms').value),
        Bathrooms: parseInt(document.getElementById('bathrooms').value),
        Year_Built: parseInt(document.getElementById('year').value),
        Location_Score: parseInt(document.getElementById('loc_score').value),
        Distance_to_City_km: parseFloat(document.getElementById('distance').value)
    };

    try {
        // 3. Send to Backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        // 4. Handle Response
        if (response.ok) {
            const data = await response.json();
            
            // Format Currency (Indian Rupee)
            const price = new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR'
            }).format(data.predicted_price);

            priceDisplay.innerText = price;
            resultBox.classList.remove('hidden');
        } else {
            alert("Error: " + response.statusText);
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server.");
    } finally {
        // 5. Reset Button
        btn.innerText = originalText;
        btn.disabled = false;
    }
});