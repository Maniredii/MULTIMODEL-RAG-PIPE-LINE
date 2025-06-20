import os   
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from fpdf import FPDF
from PIL import Image
import pytesseract
import platform
import cv2
import numpy as np
import tempfile
from file_utils import preprocess_image, extract_text_from_image, extract_text_from_pdf, process_file
from vector_utils import get_text_chunks, get_vector_store

# Configure API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Configure Tesseract path based on operating system
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
elif platform.system() == "Darwin":  # macOS
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
else:  # Linux
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Initialize sentence transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_conversational_chain(model_name):
    """
    Create a conversational chain with the selected model
    """
    prompt_template = """
    Analyze and provide insights from the given context. The content may come from 
    documents, images, or text.

    Context: {context}
    Question: {question}

    Answer:
    """
    
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

def user_input(user_question, model_name):
    vector_store = get_vector_store(get_text_chunks(user_question))
    context = "\n".join(vector_store.get_relevant_documents(user_question))
    chain = get_conversational_chain(model_name)
    response = chain.run(context=context, question=user_question)
    return response, context

def process_uploads(files):
    """
    Handle file processing and vector store creation
    """
    try:
        combined_text = ""
        for file in files:
            text = process_file(file)
            combined_text += text + "\n\n"
        
        if combined_text.strip():
            st.session_state.current_text = combined_text
            st.session_state.processing_complete = True
            st.success("Files processed successfully! You can now ask questions about the content.")
        else:
            st.error("No text could be extracted from the uploaded files.")
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
        st.session_state.processing_complete = False

def process_direct_text(text):
    """
    Handle direct text input processing
    """
    try:
        if text.strip():
            st.session_state.current_text = text
            st.session_state.processing_complete = True
            st.success("Text processed successfully! You can now ask questions about the content.")
        else:
            st.error("Please enter some text to process.")
    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        st.session_state.processing_complete = False

def main():
    st.set_page_config(
        page_title="Document Chat Assistant",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

    # Header section
    st.title("📚 Document Chat Assistant")
    
    # Input options
    input_type = st.selectbox(
        "Select Input Type",
        ["Documents", "Image", "Direct Text"],
        key="input_type_selector"
    )

    # Enhanced input sections
    if input_type == "Documents":
        uploaded_files = st.file_uploader(
            "Upload Documents (PDF, TXT, DOCX)",
            type=['pdf', 'txt', 'docx', 'doc'],
            accept_multiple_files=True,
            help="Upload one or more documents to analyze"
        )
        if uploaded_files:
            st.button("Process Documents", key="process_docs", 
                     on_click=lambda: process_uploads(uploaded_files))
    
    elif input_type == "Image":
        uploaded_images = st.file_uploader(
            "Upload Images",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            accept_multiple_files=True,
            help="Upload one or more images to analyze"
        )
        if uploaded_images:
            st.button("Process Images", key="process_images", 
                     on_click=lambda: process_uploads(uploaded_images))
    
    else:  # Direct Text
        direct_text = st.text_area(
            "Enter or paste your text here:",
            height=400,
            key="direct_text_input",
            help="Enter or paste your text here for analysis",
            placeholder="Enter or paste your text here..."
        )
        
        if direct_text.strip():
            st.button(
                "Process Text",
                key="process_text",
                on_click=lambda: process_direct_text(direct_text)
            )

    # Chat interface
    st.markdown("---")
    
    # Message container with custom styling
    message_container = st.container()
    
    with message_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
                st.markdown(message["content"])

    # Chat input
    st.markdown("---")
    if st.session_state.processing_complete:
        user_question = st.chat_input("Ask a question about the content...")
        if user_question:
            with st.spinner("Thinking..."):
                response, context = user_input(user_question, "gemini-pro")  # Default model
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_question
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                st.rerun()

if __name__ == "__main__":
    main()
