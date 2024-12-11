from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    # Fetch Surah details from the API
    api_url = "https://api.quran.com/api/v4/chapters"
    response = requests.get(api_url)

    # Parse the response JSON
    if response.status_code == 200:
        chapters = response.json().get('chapters', [])
    else:
        chapters = []

    # Pass chapters data to the home.html template
    return render_template('home.html', chapters=chapters)

@app.route('/surah/<int:surah_id>')
def surah(surah_id):
    # Fetch specific Surah details from the API
    chapter_api_url = f"https://api.quran.com/api/v4/chapters/{surah_id}"
    verses_api_url = f"https://api.quran.com/api/v4/quran/verses/uthmani?chapter_number={surah_id}"
    translation_api_url = f"https://api.quran.com/api/v4/quran/translations/131?chapter_number={surah_id}"

    chapter_response = requests.get(chapter_api_url)
    verses_response = requests.get(verses_api_url)
    translation_response = requests.get(translation_api_url)

    if chapter_response.status_code == 200:
        surah = chapter_response.json().get('chapter', {})
    else:
        surah = {}
    if verses_response.status_code == 200:
        verses = verses_response.json().get('verses', {})
    else:
        verses = []

    if translation_response.status_code == 200:
        translations = translation_response.json().get('translations', [])
    else:
        translations = []

    # Pair each verse with its translation
    verses_with_translations = [
        {
            "text_uthmani": verse.get('text_uthmani'),
            "translation": translations[index].get('text') if index < len(translations) else None
        }
        for index, verse in enumerate(verses)
    ]
        
    # Pass Surah details to the surah.html template
    return render_template('surah.html', surah=surah, verses=verses_with_translations)
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
