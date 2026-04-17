"""
OCR Smart Notes Generator
Flask backend - handles image upload, OCR, and summarization
"""

import os
import re
import cv2
import numpy as np
import requests
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64
from fpdf import FPDF

# ── App Setup ─────────────────────────────────────────
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ── Helpers ───────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    processed_path = image_path.replace('.', '_processed.')
    cv2.imwrite(processed_path, thresh)
    return processed_path


# ✅ NEW OCR FUNCTION (API BASED)
def extract_text(image_path):
    with open(image_path, 'rb') as f:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'filename': f},
            data={'apikey': 'helloworld'}  # free key
        )

    result = response.json()

    try:
        return result['ParsedResults'][0]['ParsedText']
    except:
        return ""


def clean_text(raw_text):
    lines = raw_text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if len(re.sub(r'[^a-zA-Z0-9]', '', line)) >= 3:
            cleaned_lines.append(line)

    text = ' '.join(cleaned_lines)
    text = re.sub(r' +', ' ', text)
    text = text.replace('|', 'I').replace('`', "'")

    return text.strip()


def summarize_text(text, bullet_points=False):
    if len(text.split()) < 30:
        return text

    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary = ' '.join(sentences[:3])

    if bullet_points:
        summary = '\n'.join(f'• {s.strip()}' for s in sentences[:3] if s.strip())

    return summary


def image_to_base64(path):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')

    ext = path.rsplit('.', 1)[-1].lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'

    return f'data:{mime};base64,{data}'


# ── Routes ────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    bullet = request.form.get('bullet_points', 'false') == 'true'

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    try:
        processed_path = preprocess_image(save_path)
        raw_text = extract_text(processed_path)
        clean = clean_text(raw_text)

        if not clean:
            return jsonify({'error': 'No readable text found'}), 422

        summary = summarize_text(clean, bullet_points=bullet)
        processed_b64 = image_to_base64(processed_path)

        for p in [save_path, processed_path]:
            try:
                os.remove(p)
            except:
                pass

        return jsonify({
            'extracted_text': clean,
            'summary': summary,
            'processed_image': processed_b64,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    data = request.get_json()
    text = data.get('extracted_text', '')
    summary = data.get('summary', '')

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, 'OCR Smart Notes', ln=True, align='C')
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, 'Summary', ln=True)

    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, summary)

    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, 'Extracted Text', ln=True)

    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6, text)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)

    return send_file(
        buf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='smart_notes.pdf'
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)