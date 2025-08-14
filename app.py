from flask import Flask, render_template, request, jsonify
import requests
from db import init_db, get_word, add_word
import os

app = Flask(__name__)

# Initialize the database when the app starts
with app.app_context():
    init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    translation = ''
    error = ''
    turkish_word = ''

    if request.method == 'POST':
        turkish_word = request.form['word'].strip()
        
        if not turkish_word:
            error = "Please enter a word."
        else:
            # First, check the local database (case-insensitive)
            english_word = get_word(turkish_word.lower())

            if english_word:
                translation = english_word.capitalize()
            else:
                # If not in the DB, fetch from a free API
                try:
                    # Using LibreTranslate API [1, 4]
                    response = requests.post("https://libretranslate.de/translate", json={
                        "q": turkish_word,
                        "source": "tr",
                        "target": "en"
                    }, timeout=5)
                    response.raise_for_status() # Raise an exception for bad status codes
                    
                    translation_data = response.json()
                    if "translatedText" in translation_data and translation_data["translatedText"]:
                        translated_text = translation_data["translatedText"]
                        translation = translated_text.capitalize()
                        
                        # Save the new translation to the database
                        add_word(turkish_word, translated_text)
                    else:
                        error = f"Could not find a translation for '{turkish_word}'."

                except requests.exceptions.RequestException as e:
                    error = f"Could not connect to the translation service: {e}"

    return render_template('index.html', translation=translation, error=error, searched_word=turkish_word)

if __name__ == '__main__':
    # The Docker container will run this on port 5000
    app.run(host='0.0.0.0', port=5000)
