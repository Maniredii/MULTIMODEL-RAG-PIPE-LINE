import os
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import platform
import cv2
import numpy as np

def preprocess_image(image):
    """
    Preprocess image to improve OCR accuracy
    """
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    gray = cv2.dilate(gray, kernel, iterations=1)
    return Image.fromarray(gray)

def extract_text_from_image(image_file):
    """
    Extract text from image with improved preprocessing and error handling
    """
    try:
        image = Image.open(image_file)
        st.image(image, caption="Original Image", use_column_width=True)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        processed_image = preprocess_image(image)
        st.image(processed_image, caption="Processed Image", use_column_width=True)
        text = pytesseract.image_to_string(
            processed_image,
            config='--psm 6'
        )
        if not text.strip():
            return "No text was detected in the image. Please try with a clearer image."
        st.write("Extracted Text:")
        st.write(text)
        return text
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return f"Error processing image: {str(e)}"

def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF files
    """
    try:
        text = ""
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return f"Error processing PDF: {str(e)}"

def process_file(uploaded_file):
    """
    Process different file types and extract text
    """
    try:
        file_type = uploaded_file.type
        if 'pdf' in file_type:
            return extract_text_from_pdf(uploaded_file)
        elif 'image' in file_type:
            return extract_text_from_image(uploaded_file)
        elif 'text' in file_type:
            return uploaded_file.getvalue().decode()
        else:
            return f"File type {file_type} is not supported."
    except Exception as e:
        return f"Error processing file: {str(e)}" 