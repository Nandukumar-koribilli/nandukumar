from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from googletrans import Translator
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection with provided credentials
try:
    client = MongoClient("mongodb+srv://voice_user:kumar456@cluster0.cupafkv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    client.server_info()  # Test the connection
    print("Successfully connected to MongoDB Atlas")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {str(e)}")
    raise

# Select database and collection
db = client["voice_translator"]
collection = db["translations"]

# Supported languages for detection and translation
SUPPORTED_LANGUAGES = {'en', 'te'}

# Test route for translation
@app.route('/test-translate', methods=['GET'])
def test_translate():
    try:
        translator = Translator()
        print("Attempting test translation...")
        # Test with English to Telugu
        text = "Hello, how are you?"
        detected = translator.detect(text)
        detected_lang = detected.lang.split('-')[0]  # e.g., 'en-US' -> 'en'
        target_lang = 'te' if detected_lang == 'en' else 'en'
        print(f"Detected language: {detected_lang}, Target language: {target_lang}")
        translated = translator.translate(text, dest=target_lang).text
        print(f"Test translation successful: {translated}")
        return jsonify({
            'translated_text': translated,
            'detected_lang': detected_lang,
            'target_lang': target_lang
        })
    except Exception as e:
        print(f"Test translation failed: {str(e)}")
        return jsonify({'error': f'Test translation error: {str(e)}'}), 500

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')

    print(f"Received translation request: text='{text}'")

    if not text:
        print("Missing text")
        return jsonify({'error': 'Missing text'}), 400

    try:
        # Create a new translator instance for each request
        translator = Translator()
        
        # Detect the source language
        print("Detecting source language...")
        detected = translator.detect(text)
        detected_lang = detected.lang.split('-')[0]  # e.g., 'en-US' -> 'en', 'te-IN' -> 'te'
        print(f"Detected language: {detected_lang}")

        # Validate detected language
        if detected_lang not in SUPPORTED_LANGUAGES:
            print(f"Unsupported detected language: {detected_lang}")
            return jsonify({'error': f'Unsupported detected language: {detected_lang}'}), 400

        # Determine target language: English -> Telugu, Telugu -> English
        target_lang = 'te' if detected_lang == 'en' else 'en'
        print(f"Target language: {target_lang}")

        # Retry mechanism for translation
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Translation attempt {attempt + 1}/{max_retries}")
                translated = translator.translate(text, dest=target_lang).text
                print(f"Translation successful: {translated}")
                break
            except Exception as e:
                print(f"Translation attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2)  # Wait 2 seconds before retrying
        
        if not translated:
            print("Translation failed: No result returned")
            return jsonify({'error': 'Translation failed'}), 500

        # Save translation to MongoDB
        print("Saving translation to MongoDB...")
        record = {
            "original_text": text,
            "translated_text": translated,
            "detected_language": detected_lang,
            "target_language": target_lang,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(record)
        print("Successfully saved to MongoDB")

        return jsonify({
            'translated_text': translated,
            'detected_lang': detected_lang,
            'target_lang': target_lang
        })
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return jsonify({'error': f'Translation error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)