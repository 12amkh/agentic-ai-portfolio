import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================================
# 💾 SETUP VECTOR DB
# ================================

embedder = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_documents")

# ================================
# 📄 OUR FAKE DOCUMENTS
# ================================

documents = [
    "Employees get 21 vacation days per year. Vacation must be approved by manager.",
    "The company provides health insurance for all full-time employees and their families.",
    "Remote work is allowed 3 days per week. Core hours are 10am to 3pm.",
    "Salaries are reviewed every 6 months based on performance evaluation.",
    "The office is located in Amman, Jordan. Parking is free for all employees.",
]

# ================================
# 🔢 CONVERT TO VECTORS & STORE
# ================================

for i, doc in enumerate(documents):
    embedding = embedder.encode(doc).tolist()
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[doc]
    )

print("✅ Documents stored in Vector DB!")

# ================================
# 🔍 TEST SEARCH
# ================================

query = "How many vacation days do I get?"
query_embedding = embedder.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print(f"\n🔍 Query: {query}")
print(f"📄 Most relevant chunk: {results['documents'][0][0]}")

# ================================
# 🤖 RAG FUNCTION
# ================================

def ask_rag(question: str):
    print(f"\n🔍 Question: {question}")

    query_embedding = embedder.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    context = "\n".join(results['documents'][0])
    print(f"📄 Found context: {context}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context say 'I don't know'.

Context:
{context}"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content
    print(f"✅ Answer: {answer}")
    return answer

# ================================
# 🚀 TEST IT!
# ================================

ask_rag("How many vacation days do I get?")
ask_rag("Can I work from home?")
ask_rag("What is the CEO's name?")
