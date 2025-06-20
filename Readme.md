# **Multimodal RAG (Retrieval-Augmented Generation) Application**

<div align="center">
  <img src="https://raw.githubusercontent.com/Maniredii/RAG-Application/main/assets/logo.png" alt="RAG Application Logo" width="200"/>
</div>

## **OVERVIEW**

This application is a Multimodal Retrieval-Augmented Generation (RAG) system that processes PDF documents, extracts and retrieves relevant information, and provides intelligent insights based on user queries. It uses advanced AI models for embedding generation, conversational querying, and PDF processing.

## **FEATURES**

- 📄 **PDF Text Extraction:** Extracts text from uploaded PDF documents
- 🔄 **Text Chunking:** Splits extracted text into manageable chunks for efficient processing
- 🔍 **Vector Store Creation:** Generates embeddings using Google Generative AI models and stores them in a FAISS index
- 💬 **Conversational Querying:** Answers user queries based on document content using retrieval-augmented AI models
- 📝 **Chat History:** Maintains chat history and allows users to download it as a PDF
- ⚙️ **Customizable AI Models:** Supports multiple AI models for tailored results

## **Technologies Used**

### **Programming Language:**
- Python

### **Libraries:**
- `Streamlit` - Interactive user interface
- `PyPDF2` - PDF text extraction
- `FAISS` - Vector storage and retrieval
- `LangChain` - Document splitting, chaining, and retrieval
- `Google Generative AI` - Embedding generation
- `ChatGroq` - Conversational querying
- `FPDF` - PDF generation

### **Environment:**
- API keys stored and loaded using `.env`

## **Installation Process**

1. Clone the repository
   ```bash
   git clone https://github.com/Maniredii/RAG-Application.git
   ```

2. Set up a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   streamlit run app.py
   ```

## **Usage**

1. Upload one or more PDF files via the interface
2. Click on Submit & Process to extract and process text from PDFs
3. Ask queries in the chat interface to receive accurate insights from the documents
4. Download the chat history as a PDF for later reference
5. Reset the chat history if needed

## **Model Options**

The application supports various AI models. Users can select their preferred model from the sidebar:

- ✨ Gemma2-9B
- 🚀 Llama3-70B
- 🔥 Llama 3.1 70B
- ⚡ Mixtral-8x7B

## **Features in Detail**

### **1. Text Extraction**
- Uses PyPDF2 to read and extract text from PDF pages

### **2. Chunking**
- Splits text into smaller chunks using RecursiveCharacterTextSplitter

### **3. Embedding and Vector Storage**
- Generates embeddings using Google Generative AI
- Stores them using FAISS
- Utilizes ChatGroq for querying with highly customized prompts

### **4. PDF Output**
- Generates and downloads a PDF containing the entire chat history

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## **Author**

**Manideep Reddy Eevuri**

<div align="center">
  <a href="https://www.linkedin.com/in/manideep-reddy-eevuri-661659268">
    <img src="https://img.shields.io/badge/LinkedIn-Manideep_Reddy-blue?style=flat-square&logo=linkedin" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/Maniredii">
    <img src="https://img.shields.io/badge/GitHub-Maniredii-green?style=flat-square&logo=github" alt="GitHub"/>
  </a>
</div>

## **Acknowledgments**

Thanks to the developers of the libraries and models used in this project.

---
<div align="center">
  Made with ❤️ by Manideep Reddy Eevuri
</div>
