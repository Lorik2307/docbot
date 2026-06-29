import streamlit as st
from groq import Groq
import PyPDF2
import io

# --- CONFIG ---
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="DocBot 🤖", page_icon="🤖")
st.title("🤖 DocBot — Ask Your Documents Anything")
st.write("Upload a PDF or paste text, then ask questions about it!")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
pasted_text = st.text_area("Or paste your text here", height=150)

document_text = ""

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    for page in pdf_reader.pages:
        document_text += page.extract_text()
    st.success(f"✅ PDF loaded — {len(pdf_reader.pages)} pages")

elif pasted_text:
    document_text = pasted_text
    st.success("✅ Text loaded!")

# --- Question Input ---
if document_text:
    question = st.text_input("Ask a question about your document")
    
    if st.button("Ask DocBot") and question:
        with st.spinner("Thinking..."):
            prompt = f"""You are a helpful assistant. Answer the question based ONLY on the document below.
            
Document:
{document_text}

Question: {question}

Answer:"""
            
            response = client.chat.completions.create(
               model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            
            answer = response.choices[0].message.content
            st.markdown("### 💬 Answer")
            st.write(answer)