import gradio as gr
import pdfplumber
import docx
import os
import datetime
from transformers import pipeline

# Load open-source LLMs
summary_llm = pipeline("summarization", model="google/pegasus-xsum", tokenizer="google/pegasus-xsum")
text_llm = pipeline("text2text-generation", model="MBZUAI/LaMini-T5-738M", tokenizer="MBZUAI/LaMini-T5-738M")

# Extract text from files
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file.name) as pdf:
            return "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return "Unsupported file format."

# Format glossary visually
def format_glossary_html(glossary_text):
    lines = glossary_text.split('\n')
    html = ""
    for line in lines:
        if ":" in line:
            term, desc = line.split(":", 1)
            html += f"<b style='color:#1e3a8a'>{term.strip()}</b>: {desc.strip()}<br>"
        else:
            html += f"{line}<br>"
    return html

# Generate summary
def generate_summary(text):
    return summary_llm(text[:1024], max_length=250, min_length=80, do_sample=False)[0]["summary_text"]

# Generate text (glossary/verdict/custom)
def generate_text_response(prompt, max_len=512):
    return text_llm(prompt, max_length=max_len, do_sample=True)[0]["generated_text"]

# Main document analyzer
def analyze_document(file):
    filename = os.path.basename(file.name)
    text = extract_text(file)
    if not text.strip():
        return "No content found in file.", "", "", "", "", None, ""

    short_text = text[:3000]

    # Enhanced prompts
    summary_prompt = f"""
You are a legal assistant. Read the following legal document and generate a comprehensive summary.

Include: parties involved, key facts, legal issues, arguments, court observations, and likely outcome.

Document:
{short_text}
"""
    glossary_prompt = f"""
Extract and explain all legal terms, laws, or references. Format:

Term: ...
Explanation: ...

Document:
{short_text}
"""
    verdict_prompt = f"""
Based on the document, predict the likely verdict in 2–3 sentences using standard legal reasoning.

Document:
{short_text}
"""

    # Run LLMs
    summary = generate_summary(short_text)
    glossary = generate_text_response(glossary_prompt)
    verdict = generate_text_response(verdict_prompt)
    glossary_html = format_glossary_html(glossary)

    # Save report
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"LegalSummary_{timestamp}.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(f"📄 File: {filename}\n🕒 Time: {timestamp}\n\n")
        f.write("=== 📑 Summary ===\n" + summary + "\n\n")
        f.write("=== 📘 Glossary ===\n" + glossary + "\n\n")
        f.write("=== ⚖️ Verdict ===\n" + verdict + "\n")

    return text, summary, glossary, glossary_html, verdict, output_filename, short_text

# Custom prompt answer
def custom_prompt_response(doc_text, user_prompt):
    if not doc_text.strip() or not user_prompt.strip():
        return "⚠️ Please provide both a document and a prompt."
    prompt = f"""
You are a legal expert. Answer the question below using only the document provided.

Question:
{user_prompt.strip()}

Document:
{doc_text.strip()}
"""
    return generate_text_response(prompt)

# Gradio UI
with gr.Blocks(css="body { background-color: #f9f9f9; font-family: 'Segoe UI'; }") as demo:
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("""
<div style='text-align: center; font-size: 28px; font-weight: bold; color: #1e3a8a; margin-bottom: 10px;'>
🧾 Legal Document Summarizer Using LLMs
</div>
<div style='text-align: center; font-size: 16px; color: #444444; margin-bottom: 25px;'>
Upload legal documents in PDF, DOCX, or TXT format to receive structured summaries, legal term glossaries, and AI-inferred verdicts using open-source language models.
</div>
""")
            file_input = gr.File(label="📁 Upload Legal Document")
            submit_btn = gr.Button("🔍 Analyze Document")
            download_btn = gr.File(label="⬇️ Download Report")

        with gr.Column(scale=1):
            gr.Markdown("### 💡 Features")
            gr.Markdown("""
- 📝 AI-generated legal summaries  
- 📘 Glossary of legal terms  
- ⚖️ Inferred legal verdict  
- ❓ Custom Q&A based on the document
""")

    extracted = gr.Textbox(label="📄 Extracted Text", lines=10, interactive=False)
    summary = gr.Textbox(label="📝 Summary", lines=6, interactive=False)
    glossary_raw = gr.Textbox(visible=False)
    glossary_html = gr.HTML(label="📘 Glossary of Legal Terms")
    final_verdict = gr.Textbox(label="⚖️ Verdict (AI Inferred)", lines=3, interactive=False)

    with gr.Row():
        gr.Markdown("### ❓ Ask a Question About the Document")
    user_prompt = gr.Textbox(label="Your Question", placeholder="e.g., What is the legal issue?")
    custom_response = gr.Textbox(label="🤖 AI Answer", lines=4)
    custom_btn = gr.Button("🧠 Get Answer")
    hidden_doc_text = gr.Textbox(visible=False)

    submit_btn.click(fn=analyze_document, inputs=[file_input], outputs=[
        extracted, summary, glossary_raw, glossary_html, final_verdict, download_btn, hidden_doc_text
    ])
    custom_btn.click(fn=custom_prompt_response, inputs=[hidden_doc_text, user_prompt], outputs=custom_response)

demo.launch()
