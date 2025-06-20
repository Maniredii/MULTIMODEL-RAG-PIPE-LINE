from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = sentence_model.encode(text_chunks)
    def retrieve_similar_chunks(query, k=2):
        query_embedding = sentence_model.encode([query])
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        top_k_indices = similarities.argsort()[-k:][::-1]
        return [text_chunks[i] for i in top_k_indices]
    class SimpleRetriever:
        def get_relevant_documents(self, query):
            return retrieve_similar_chunks(query)
    return SimpleRetriever() 