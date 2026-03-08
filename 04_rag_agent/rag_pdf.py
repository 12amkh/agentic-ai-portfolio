import os
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedder = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="pdf_documents")

# ================================
# 📄 READ & CHUNK THE PDF
# ================================

def load_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)
    chunks = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            words = text.split()
            chunk = ""
            for word in words:
                chunk += word + " "
                if len(chunk) > 500:
                    chunks.append(chunk.strip())
                    chunk = ""
            if chunk:
                chunks.append(chunk.strip())

    print(f"✅ Loaded {len(chunks)} chunks from PDF")
    return chunks

# ================================
# 💾 STORE IN VECTOR DB
# ================================

def store_chunks(chunks: list):
    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk]
        )
    print(f"✅ Stored {len(chunks)} chunks in Vector DB!")

# ================================
# 🤖 RAG FUNCTION
# ================================

def ask_pdf(question: str):
    print(f"\n🔍 Question: {question}")

    query_embedding = embedder.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context = "\n".join(results['documents'][0])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful assistant analyzing a document.
Answer the question using the context below.
If the context gives any clues — use them to give your best answer.
Only say 'I don't know' if the context has absolutely nothing relevant.

Context:
{context}"""
            },
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content
    print(f"✅ Answer: {answer}\n")
    return answer

# ================================
# 🚀 RUN IT
# ================================

pdf_path = "Function discussion.pdf"

if not os.path.isfile(pdf_path):
    candidates = [f for f in os.listdir(".") if f.lower().startswith("function discussion") and f.lower().endswith(".pdf")]
    if candidates:
        pdf_path = candidates[0]
        print(f"Using detected PDF: {pdf_path}")
    else:
        raise FileNotFoundError(f"Could not find '{pdf_path}' in the current directory.")

chunks = load_pdf(pdf_path)
store_chunks(chunks)

ask_pdf("What hardware components are mentioned?")
ask_pdf("What is the purpose of this project?")
ask_pdf("What camera is used in this page?")
ask_pdf("What does this project detect?")


