from flask import Flask, render_template, request
import speech_recognition as sr
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'audio' not in request.files:
        return "No audio file uploaded", 400

    file = request.files['audio']
    recognizer = sr.Recognizer()

    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
        except:
            return "Could not understand audio", 400

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        emotion = "Positive"
    elif polarity < 0:
        emotion = "Negative"
    else:
        emotion = "Neutral"

    return f"Detected Emotion: {emotion}<br><br>Transcript: {text}"

if __name__ == '__main__':
    app.run(debug=True)
