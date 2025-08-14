from flask import Flask, render_template, request
import requests
from db import init_db, get_word, add_word

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    translation = ''
    if request.method == 'POST':
        turkish_word = request.form['word']
        
        # First, check the local database
        english_word = get_word(turkish_word)

        if english_word:
            translation = english_word
        else:
            # If not in the DB, fetch from a free API
            # Using LibreTranslate API here. [1, 4]
            response = requests.post("https://libretranslate.de/translate", json={
                "q": turkish_word,
                "source": "tr",
                "target": "en"
            })
            
            if response.status_code == 200:
                translation_data = response.json()
                if "translatedText" in translation_data:
                    translated_text = translation_data["translatedText"]
                    translation = translated_text
                    
                    # Save the new translation to the database
                    add_word(turkish_word, translated_text)

    return render_template('index.html', translation=translation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
