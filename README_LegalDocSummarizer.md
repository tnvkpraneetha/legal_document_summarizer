# 🧾 Legal Document Summarizer Using LLMs

An AI-powered web application that simplifies complex legal documents by generating structured summaries, glossaries of legal terms, and inferred verdicts — all through open-source Large Language Models (LLMs). Built using Gradio and deployed on Hugging Face Spaces.

---

## 🚀 Features

✅ Upload Legal Documents – Supports PDF, DOCX, and TXT formats  
✅ AI-Generated Summary – Highlights key facts, parties, issues, and arguments  
✅ Glossary of Legal Terms – Extracted and explained in plain language  
✅ AI-Inferred Verdict – Predicts the likely legal outcome using reasoning  
✅ Custom Q&A – Ask any legal question based on the uploaded document  
✅ Downloadable Report – Generates a structured `.txt` file of all outputs  
✅ Interactive Gradio UI – Clean, fast, and user-friendly interface

---

## 🧠 How It Works

This project uses two Hugging Face transformer models:

- `google/pegasus-xsum` – for abstractive legal document summarization  
- `MBZUAI/LaMini-T5-738M` – for glossary generation, verdict prediction, and Q&A  

The app first extracts the text content from uploaded files using `pdfplumber` or `python-docx`, then feeds prompts to the language models for generation.

---

## 🛠️ Tech Stack

| Component       | Technology                         |
|----------------|-------------------------------------|
| Interface       | Gradio                             |
| LLMs            | Pegasus XSum, LaMini-T5-738M       |
| Text Extraction | pdfplumber, python-docx            |
| Backend         | Python                             |
| Deployment      | Hugging Face Spaces                |

---

## 📂 File Structure

```
├── app.py            # Main Gradio app  
├── requirements.txt  # Python dependencies  
├── README.md         # Project documentation  
```

---

## 📦 Installation

```bash
git clone https://github.com/your-username/legal-document-summarizer
cd legal-document-summarizer
pip install -r requirements.txt
python app.py
```

The app will launch locally at: [http://localhost:7860](http://localhost:7860)

---

## 🌐 Live Demo

Try it now on Hugging Face Spaces:  
🔗 https://huggingface.co/spaces/Pradeepthi30/legal-doc-llms

---

## 📁 Example Output

**Summary:**  
Summarizes key aspects of the document.

**Glossary:**  
Explains terms like _res judicata_, _amicus curiae_, etc.

**Verdict:**  
> “The court is likely to dismiss the case due to insufficient evidence.”

**Q&A:**  
“What is the central issue in this case?” → _[AI-generated answer]_

---

## 🎓 Academic & Internship Credit

This project was developed as a **final internship project** at **Neubalitics Tech Pvt. Ltd.** in collaboration with **Sathyabama Institute of Science & Technology, Chennai**.  
**Mentored by:** *Nethaji N.*  
**Coordinated by:** *Danush Rajaram*

---

## 🙌 Acknowledgements

- Hugging Face 🤗 Transformers community  
- Open-source contributors  
- Neubalitics AI R&D team

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to use, modify, and build upon it.
