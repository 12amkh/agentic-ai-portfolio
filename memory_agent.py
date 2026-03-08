from groq import Groq
from dotenv import load_dotenv
import os

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================================
# 🧠 MEMORY — conversation history
# ================================

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# First question
messages.append({"role": "user", "content": "What is the capital of UAE?"})

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages
)

answer = response.choices[0].message.content
messages.append({"role": "assistant", "content": answer})
print(f"Assistant: {answer}")

# Second question — references the first!
messages.append({"role": "user", "content": "What is the population of that city?"})

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages
)

answer = response.choices[0].message.content
print(f"Assistant: {answer}")
