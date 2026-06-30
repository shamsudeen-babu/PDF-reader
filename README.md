# 📄 Chat with your PDF

A beginner-friendly Streamlit app that lets you upload a PDF and ask questions about it using AI.

---

## 📸 What It Does

Upload any text-based PDF and ask it questions in plain English — the AI reads the document and answers based on its content.

- ✅ Upload a single PDF file
- ✅ Extracts text from all pages
- ✅ Ask any question about the PDF content
- ✅ AI answers using Groq's LLM (GPT-OSS model)
- ✅ Shows word count of the uploaded PDF
- ✅ Handles scanned/unreadable PDFs gracefully
- ✅ Clean and simple web interface using Streamlit

---

## 🛠️ Libraries Used

| Library | Why |
|--------|-----|
| `streamlit` | Builds the web app interface |
| `PyPDF2` | Reads and extracts text from PDF |
| `langchain_text_splitters` | Splits PDF text into chunks |
| `langchain_groq` | Connects to Groq's LLM |
| `langchain_core` | Prompt templates & output parsing |

---

## ⚙️ Installation

Make sure Python is installed, then run:

```bash
pip install streamlit PyPDF2 langchain langchain-groq langchain-core
```

---

## 🔑 Setup API Key

This project uses **Groq API** for AI responses.

1. Get a free API key from [console.groq.com](https://console.groq.com)
2. Set it as an environment variable:

**Windows (Command Prompt):**
```bash
set GROQ_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```bash
$env:GROQ_API_KEY="your_api_key_here"
```

---

## 📂 Project Structure