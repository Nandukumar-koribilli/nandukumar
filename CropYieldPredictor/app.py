from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Dummy pre-trained model (replace with real training data and model)
# Features: [soil_quality, crop_type_encoded, season_encoded, soil_type_encoded, state_encoded]
X_train = np.array([
    [7, 0, 0, 0, 0],  # Wheat, Summer, Loam, Andhra Pradesh
    [8, 1, 1, 1, 1],  # Corn, Winter, Clay, Arunachal Pradesh
    [6, 2, 2, 2, 2],  # Rice, Autumn, Sandy, Assam
    [6, 3, 3, 3, 3],  # Barley, Spring, Silty, Bihar
    [7, 4, 4, 0, 4],  # Tomatoes, Monsoon, Loam, Chhattisgarh
    [6, 5, 0, 1, 5],  # Carrots, Summer, Clay, Goa
    [5, 6, 1, 2, 6],  # Lettuce, Winter, Sandy, Gujarat
    [8, 7, 2, 3, 7],  # Potatoes, Autumn, Silty, Haryana
    [7, 8, 3, 4, 8],  # Cucumbers, Spring, Chalk, Himachal Pradesh
    [6, 9, 4, 5, 9],  # Apples, Monsoon, Peat, Jharkhand
    [7, 10, 0, 0, 10], # Bananas, Summer, Loam, Karnataka
    [6, 11, 1, 1, 11], # Oranges, Winter, Clay, Kerala
    [5, 12, 2, 2, 12], # Strawberries, Autumn, Sandy, Madhya Pradesh
    [6, 13, 3, 3, 13], # Grapes, Spring, Silty, Maharashtra
    [7, 14, 4, 4, 14]  # Soybeans, Monsoon, Chalk, Manipur
])
y_train = np.array([5.0, 6.5, 4.8, 4.0, 3.5, 2.0, 1.5, 6.0, 4.0, 3.0, 5.5, 4.5, 2.5, 3.5, 3.5])
model = LinearRegression()
model.fit(X_train, y_train)

# Encodings
crop_types = {
    # Grains
    'wheat': 0, 'corn': 1, 'rice': 2, 'barley': 3, 'oats': 4, 'brown_rice': 5, 'white_rice': 6,
    'rye': 7, 'millet': 8,
    # Vegetables
    'potatoes': 9, 'onion': 10, 'tomatoes': 11, 'cabbage': 12, 'bean': 13, 'eggplant': 14,
    'cauliflower': 15, 'cucumbers': 16, 'frozen_peas': 17, 'garlic': 18, 'okra': 19,
    'beetroot': 20, 'green_pepper': 21, 'baby_spinach': 22, 'cloves': 23, 'cucurbits': 24,
    'carrots': 25, 'lettuce': 26,
    # Fruits
    'mango': 27, 'banana': 28, 'papaya': 29, 'guava': 30, 'pineapple': 31, 'jackfruit': 32,
    'custard_apple': 33, 'sapota': 34, 'coconut': 35, 'watermelon': 36, 'muskmelon': 37,
    'blackberry': 38, 'gooseberry': 39, 'litchi': 40, 'avocado': 41, 'orange': 42,
    'lemon': 43, 'apple': 44, 'grapes': 45, 'pomegranate': 46, 'peach': 47, 'plum': 48,
    'apricot': 49, 'mulberry': 50, 'strawberries': 51, 'dragon_fruit': 52, 'kiwi_fruit': 53,
    # Legumes
    'soybeans': 54, 'bean': 13  # Bean is both a vegetable and legume, using same encoding
}

seasons = {'summer': 0, 'winter': 1, 'autumn': 2, 'spring': 3, 'monsoon': 4}
soil_types = {'loam': 0, 'clay': 1, 'sandy': 2, 'silty': 3, 'chalk': 4, 'peat': 5}
states = {
    'andhra_pradesh': 0, 'arunachal_pradesh': 1, 'assam': 2, 'bihar': 3, 'chhattisgarh': 4,
    'goa': 5, 'gujarat': 6, 'haryana': 7, 'himachal_pradesh': 8, 'jharkhand': 9,
    'karnataka': 10, 'kerala': 11, 'madhya_pradesh': 12, 'maharashtra': 13, 'manipur': 14,
    'meghalaya': 15, 'mizoram': 16, 'nagaland': 17, 'odisha': 18, 'punjab': 19,
    'rajasthan': 20, 'sikkim': 21, 'tamil_nadu': 22, 'telangana': 23, 'tripura': 24,
    'uttar_pradesh': 25, 'uttarakhand': 26, 'west_bengal': 27
}

# Dummy data for duration (in months) and market price (in ₹ per ton)
crop_info = {
    # Grains
    'wheat': {'duration': 4, 'market_price': 20000},
    'corn': {'duration': 5, 'market_price': 18000},
    'rice': {'duration': 4, 'market_price': 25000},
    'barley': {'duration': 4, 'market_price': 19000},
    'oats': {'duration': 4, 'market_price': 22000},
    'brown_rice': {'duration': 4, 'market_price': 26000},
    'white_rice': {'duration': 4, 'market_price': 24000},
    'rye': {'duration': 4, 'market_price': 21000},
    'millet': {'duration': 3, 'market_price': 23000},
    # Vegetables
    'potatoes': {'duration': 4, 'market_price': 15000},
    'onion': {'duration': 4, 'market_price': 20000},
    'tomatoes': {'duration': 3, 'market_price': 30000},
    'cabbage': {'duration': 3, 'market_price': 18000},
    'bean': {'duration': 3, 'market_price': 25000},
    'eggplant': {'duration': 3, 'market_price': 28000},
    'cauliflower': {'duration': 3, 'market_price': 22000},
    'cucumbers': {'duration': 3, 'market_price': 35000},
    'frozen_peas': {'duration': 3, 'market_price': 40000},
    'garlic': {'duration': 6, 'market_price': 60000},
    'okra': {'duration': 3, 'market_price': 32000},
    'beetroot': {'duration': 3, 'market_price': 25000},
    'green_pepper': {'duration': 3, 'market_price': 34000},
    'baby_spinach': {'duration': 2, 'market_price': 45000},
    'cloves': {'duration': 6, 'market_price': 80000},
    'cucurbits': {'duration': 3, 'market_price': 30000},
    'carrots': {'duration': 3, 'market_price': 25000},
    'lettuce': {'duration': 2, 'market_price': 40000},
    # Fruits
    'mango': {'duration': 6, 'market_price': 60000},
    'banana': {'duration': 12, 'market_price': 45000},
    'papaya': {'duration': 9, 'market_price': 40000},
    'guava': {'duration': 6, 'market_price': 35000},
    'pineapple': {'duration': 12, 'market_price': 50000},
    'jackfruit': {'duration': 6, 'market_price': 30000},
    'custard_apple': {'duration': 6, 'market_price': 55000},
    'sapota': {'duration': 6, 'market_price': 45000},
    'coconut': {'duration': 12, 'market_price': 20000},
    'watermelon': {'duration': 3, 'market_price': 15000},
    'muskmelon': {'duration': 3, 'market_price': 25000},
    'blackberry': {'duration': 6, 'market_price': 70000},
    'gooseberry': {'duration': 6, 'market_price': 40000},
    'litchi': {'duration': 6, 'market_price': 65000},
    'avocado': {'duration': 12, 'market_price': 80000},
    'orange': {'duration': 6, 'market_price': 48000},
    'lemon': {'duration': 6, 'market_price': 30000},
    'apple': {'duration': 6, 'market_price': 50000},
    'grapes': {'duration': 6, 'market_price': 55000},
    'pomegranate': {'duration': 6, 'market_price': 60000},
    'peach': {'duration': 6, 'market_price': 65000},
    'plum': {'duration': 6, 'market_price': 60000},
    'apricot': {'duration': 6, 'market_price': 70000},
    'mulberry': {'duration': 6, 'market_price': 55000},
    'strawberries': {'duration': 3, 'market_price': 60000},
    'dragon_fruit': {'duration': 12, 'market_price': 90000},
    'kiwi_fruit': {'duration': 12, 'market_price': 85000},
    # Legumes
    'soybeans': {'duration': 4, 'market_price': 30000},
    'bean': {'duration': 3, 'market_price': 25000}  # Same as vegetable bean
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        crop_type = crop_types[data['cropType']]
        season = seasons[data['season']]
        soil_type = soil_types[data['soilType']]
        soil_quality = float(data['soilQuality'])
        land_area = float(data['landArea'])
        state = states[data['state']]

        # Prepare input for model
        input_data = np.array([[soil_quality, crop_type, season, soil_type, state]])
        predicted_yield = model.predict(input_data)[0]

        # Get crop info
        crop_name = data['cropType']
        duration = crop_info[crop_name]['duration']
        market_price = crop_info[crop_name]['market_price']

        # Calculate total yield and revenue in INR
        total_yield = predicted_yield * land_area
        revenue = total_yield * market_price

        # Dummy cost per hectare in INR (replace with real data)
        cost_per_hectare = 40000  # Approx ₹40,000/hectare
        total_cost = cost_per_hectare * land_area
        profit_or_loss = revenue - total_cost

        return jsonify({
            'cropType': crop_name.replace('_', ' ').capitalize(),
            'duration': duration,
            'yield': round(predicted_yield, 2),
            'marketPrice': market_price,
            'profitOrLoss': round(profit_or_loss, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)