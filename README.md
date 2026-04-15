# OCR Smart Notes Generator

A web app that extracts text from images using OCR and generates an AI summary.

**Stack:** Flask · pytesseract · OpenCV · DistilBART (HuggingFace) · fpdf2

---

## Project Structure

```
ocr-notes-app/
├── app.py                  ← Flask backend
├── requirements.txt
├── uploads/                ← Temp storage (auto-created)
├── templates/
│   └── index.html          ← Single-page UI
└── static/
    └── style.css
```

---

## 1 · Install Tesseract OCR (system dependency)

Tesseract must be installed **before** the Python packages.

### macOS
```bash
brew install tesseract
```

### Ubuntu / Debian
```bash
sudo apt update && sudo apt install -y tesseract-ocr
```

### Windows
1. Download the installer from:
   https://github.com/UB-Mannheim/tesseract/wiki
2. Run it (default path: `C:\Program Files\Tesseract-OCR\`)
3. Add that path to your **System PATH** environment variable
4. In `app.py`, add this line right after the imports if auto-detection fails:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

Verify installation:
```bash
tesseract --version
```

---

## 2 · Set up a Python virtual environment

```bash
cd ocr-notes-app
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

## 3 · Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Tip — CPU-only PyTorch (smaller download):**
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```
> Then run `pip install -r requirements.txt` afterwards.

The first run will download the DistilBART model (~500 MB) from HuggingFace
and cache it locally. Subsequent runs are fast.

---

## 4 · Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## Usage

1. Drag & drop (or click to browse) a JPG/PNG image
2. Toggle **Bullet-point summary** if you want a list format
3. Click **Extract & Summarize**
4. Wait ~10–30 s (first run downloads the model; later runs are faster)
5. View the extracted text and AI summary
6. Click **Copy** on either card, or **Download as PDF**

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `TesseractNotFoundError` | Check Tesseract is installed and on PATH |
| Model download hangs | Check internet connection; ~500 MB needed once |
| Blurry/noisy images produce bad OCR | Use higher-resolution scans |
| `CUDA not found` warning | Normal on CPU — the model runs on CPU by default |
| Port 5000 in use (macOS) | `python app.py` uses port 5000; disable AirPlay Receiver in System Settings |

---

## Optional: change the summarization model

In `app.py` → `get_summarizer()`, swap the model name:

| Model | Size | Notes |
|---|---|---|
| `sshleifer/distilbart-cnn-12-6` | ~500 MB | Default, fast |
| `facebook/bart-large-cnn` | ~1.6 GB | Higher quality |
| `philschmid/distilbart-cnn-12-6-samsum` | ~500 MB | Better for conversations |
