from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import random
import re
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in a .env file or environment.")

genai.configure(api_key=GEMINI_API_KEY)

# Knowledge base for specific India-related or static responses (e.g., images)
knowledge_base = {
    "createimage": {"type": "image", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Flag_of_India.svg/1200px-Flag_of_India.svg.png"},
    "indianflag": {"type": "image", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Flag_of_India.svg/1200px-Flag_of_India.svg.png"},
}

# Greeting and farewell responses
greetings = ["Hello! How can I assist you today?", "Hi there! Ask me anything!"]
farewells = ["Goodbye! Hope to chat again soon.", "Thanks for asking! See you later!"]

def get_gemini_response(user_input):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        return {"response": f"Error: {str(e)}. Please try again later.", "type": "text"}

# Function to process user input and generate a response
def get_response(user_input):
    user_input = user_input.lower().strip()

    # Check for greetings or farewells
    if user_input in ["hi", "hello", "hey"]:
        return {"response": random.choice(greetings), "type": "text"}
    elif user_input in ["bye", "goodbye", "exit"]:
        return {"response": random.choice(farewells), "type": "text"}

    # Check for specific static responses (e.g., images)
    for key, value in knowledge_base.items():
        if re.search(key, user_input):
            return value

    # Use Gemini for dynamic responses to general questions
    return {"response": get_gemini_response(user_input), "type": "text"}

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle chatbot messages
@app.route('/get_response', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"response": "No input provided.", "type": "text"}), 400
    
    response = get_response(user_input)
    return jsonify(response)

if __name__ == "__main__":
    # Use environment variable for port and host, default to 5000 and 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host=host, port=port, debug=debug)