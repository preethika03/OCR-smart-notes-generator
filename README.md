# 🧠 OCR Smart Notes Generator

An intelligent web application that extracts text from images (printed + handwritten) and generates concise AI-powered summaries.

🔗 **Live Demo:** https://ocr-smart-notes-generator-3.onrender.com

---

## 🚀 Features

* 📷 Upload image (JPG, PNG, etc.)
* ✍️ Extract text from:

  * Printed text (OCR)
  * Handwritten text (AI-based recognition)
* 🧠 Generate smart summaries
* 📄 Download results as PDF
* 🔘 Optional bullet-point summaries
* ⚡ Clean and user-friendly interface

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Image Processing:** OpenCV
* **OCR Engines:**

  * OCR.space API (Printed text)
  * Hugging Face (TrOCR model for handwritten text)
* **Frontend:** HTML, CSS
* **PDF Generation:** FPDF
* **Deployment:** Render

---

## ⚙️ How It Works

1. User uploads an image
2. Image is preprocessed (grayscale + denoise)
3. Text extraction pipeline:

   * Handwritten → Hugging Face TrOCR model
   * Printed → OCR.space API
4. Extracted text is cleaned
5. AI summary is generated
6. Results displayed + optional PDF download

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/preethika03/OCR-smart-notes-generator.git
cd OCR-smart-notes-generator

pip install -r requirements.txt
```

### ▶️ Run the app

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Environment Variables

Create a `.env` or set environment variables:

```
HF_TOKEN=your_huggingface_token_here
```

---

## 📁 Project Structure

```
OCR-NOTES-APP/
│── static/
│   └── style.css
│── templates/
│   └── index.html
│── uploads/
│── app.py
│── requirements.txt
│── README.md
```

---

## ⚠️ Limitations

* Handwritten OCR may not be 100% accurate (depends on image quality)
* Complex cursive writing may produce imperfect results
* Free APIs may have rate limits

---

## 💡 Future Improvements

* Better handwriting recognition models
* Multi-language support
* Note organization & saving system
* Mobile optimization

---

## 🙌 Acknowledgements

* Hugging Face 🤗
* OCR.space API
* OpenCV

---

## 👩‍💻 Author

**Preethika**
IT Engineering Student

---

⭐ If you like this project, give it a star!
