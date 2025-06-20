# 📋 Form APR Reconciler - powered by Regality

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![License](https://img.shields.io/badge/License-Private-green.svg)

**Version:** v1.0  
**Author:** Srinivas Maddury  
**Date:** June 17, 2025

---

## 🧠 Overview

This application reviews filled-in Form APRs (Annual Performance Reports) submitted under India's Overseas Investment (FEMA, 1999; OI Rules, 2022). It uses Mistral's cloud API (including mistral-ocr-latest) to scan each field, flag issues, and recommend corrections.

The app connects to Mistral's cloud service via API for AI processing.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- Mistral API key ([Get one here](https://console.mistral.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Regal-Forms-Form-APR
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and replace `your_mistral_api_key_here` with your actual Mistral API key.

4. **Run the application**
   ```bash
   streamlit run app.py --server.address=127.0.0.1
   ```

5. **Open in browser**
   Navigate to: http://localhost:8501

---

## 📁 How to Use

1. **Upload Documents**
   - Upload a filled Form APR (PDF format)
   - Optionally upload supporting documents (PDFs, XLSX, CSV)

2. **Configure Analysis**
   - Choose AI model (default: Mistral OCR)
   - Adjust "Analysis Creativity" slider (0 = strict, 1 = creative)

3. **Review Results**
   - ✅ Executive Summary
   - ✅ Field-by-field issues
   - ✅ Missing-docs checklist
   - ✅ FEMA rule violations
   - ✅ Download review summary as .txt file

---

## 🛠 Technical Stack

- **Frontend:** Streamlit
- **PDF Processing:** PyMuPDF (fitz)
- **AI/ML:** Mistral AI API
- **Configuration:** python-dotenv

---

## 📦 Project Structure

```
Regal-Forms-Form-APR/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── .streamlit/
    └── secrets.toml      # Streamlit configuration
```

---

## 🔐 Security Features

- ✅ AI processing via secure Mistral API connection (HTTPS)
- ✅ API keys stored locally in environment variables
- ✅ Document processing in memory only
- ✅ No persistent storage of uploaded documents
- ✅ Sensitive files excluded from version control

---

## 💡 Troubleshooting

### Common Issues

**App doesn't load?**
- Try accessing: http://127.0.0.1:8501
- Use Google Chrome (not Safari)
- Check console for errors

**API Connection failed?**
- Verify Mistral API key in `.env` file
- Check internet connection
- Ensure API key has sufficient credits

**PDF upload issues?**
- Maximum file size: 10MB
- Supported format: PDF only
- Ensure file is not corrupted

---

## 🚀 Development Roadmap

- ✅ **Phase 1:** Reconciler (current)
- 🔜 **Phase 2:** Form Filler
- 🔜 **Phase 3:** FEMA Q&A Chatbot (RAG based)

---

## 📊 API Usage

This application uses the following Mistral AI models:
- `mistral-ocr-latest` - For OCR processing
- `mistral-large-latest` - For comprehensive analysis
- `mistral-medium-latest` - For balanced performance

---

## 🛟 Support

For technical support or questions, please contact: [Insert your email]

---

## ⚖️ License

This project is private and proprietary. Unauthorized copying, distribution, or modification is prohibited.

---

## 🔄 Environment Setup

### Required Environment Variables

```bash
# Mistral API Configuration
MISTRAL_API_KEY=your_actual_api_key_here
MISTRAL_MODEL=mistral-ocr-latest
```

### Optional Streamlit Configuration

Create `.streamlit/secrets.toml` for deployment:
```toml
[default]
MISTRAL_API_KEY = "your_api_key_here"
```

---

*Built with ❤️ for regulatory compliance automation*
