from flask import Flask, render_template, request, send_file
import os
import fitz  # PyMuPDF
from gtts import gTTS

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    text = extract_text_from_pdf(filepath)
    audio_path = text_to_speech(text, file.filename)
    return send_file(audio_path, as_attachment=True)


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()


def text_to_speech(text, filename):
    if not text.strip():
        return "No text found in the PDF"
    
    tts = gTTS(text)
    audio_path = os.path.join(UPLOAD_FOLDER, f"{filename}.mp3")
    tts.save(audio_path)
    return audio_path

if __name__ == '__main__':
    app.run(debug=True)
