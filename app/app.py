from flask import Flask, render_template, request
import requests
from db import init_db, get_word, add_word

app = Flask(__name__)

# Initialize the database when the app starts
with app.app_context():
    init_db()

def translate_word(word):
    """
    Translates a word using the MyMemory API.
    Returns the translated text or None if translation fails.
    """
    try:
        # Using MyMemory API - free for anonymous use
        url = f"https://api.mymemory.translated.net/get?q={word}&langpair=tr|en"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        
        # Check if the API call was successful and translation is available
        if data and data.get("responseStatus") == 200:
            translated_text = data["responseData"]["translatedText"]
            return translated_text
        else:
            # Handle cases where the API returns an error in the JSON
            # e.g., "NO QUERY SPECIFIED"
            return None
            
    except requests.exceptions.RequestException:
        # Handles connection errors, timeouts, etc.
        return None
    except (ValueError, KeyError):
        # Handles JSON decoding errors or unexpected JSON structure
        return None

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
                # If not in the DB, fetch from the external API
                translated_text = translate_word(turkish_word)
                
                if translated_text:
                    translation = translated_text.capitalize()
                    # Save the new translation to the database
                    add_word(turkish_word, translated_text)
                else:
                    error = f"Translation failed. Could not find or translate the word '{turkish_word}'."

    return render_template('index.html', translation=translation, error=error, searched_word=turkish_word)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
