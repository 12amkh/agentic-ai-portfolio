from groq import Groq

client = Groq(api_key="your_api_key_here")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "What is the capital of Jordan?"}
    ]
)

print(response.choices[0].message.content)