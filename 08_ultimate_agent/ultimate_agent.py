import os
import json
import chromadb
from groq import Groq
from tavily import TavilyClient
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END
from typing import TypedDict
from dotenv import load_dotenv

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
embedder = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="ultimate_docs")

# ================================
# 📄 LOAD PDF INTO VECTOR DB
# ================================

def load_pdf(pdf_path: str):
    if not os.path.exists(pdf_path):
        print(f"⚠️ PDF not found: {pdf_path}")
        return

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

    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk]
        )

    print(f"✅ Loaded {len(chunks)} chunks from PDF!")

# ================================
# 🛠️ TOOLS
# ================================

def search_pdf(query: str) -> str:
    print(f"📄 Searching PDF: {query}")
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    if results['documents'][0]:
        return "\n".join(results['documents'][0])
    return "Nothing relevant found in PDF."

def search_web(query: str) -> str:
    print(f"🔍 Searching web: {query}")
    results = tavily_client.search(query, max_results=3)
    output = ""
    for r in results['results']:
        output += f"Title: {r['title']}\n"
        output += f"Content: {r['content']}\n\n"
    return output

def calculate(expression: str) -> str:
    print(f"🧮 Calculating: {expression}")
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

# ================================
# 🧰 TOOLS DEFINITION
# ================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_pdf",
            "description": "Search the uploaded PDF document for relevant information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to search for in the PDF"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the internet for current real-world information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate any math expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"]
            }
        }
    }
]

# ================================
# 🧠 STATE
# ================================

class AgentState(TypedDict):
    task: str
    messages: list
    final_answer: str
    iteration: int

# ================================
# 🔷 NODES
# ================================

def agent_node(state: AgentState) -> AgentState:
    print(f"\n🧠 Agent thinking... (iteration {state['iteration']})")

    # Keep context clean
    messages_to_send = [state['messages'][0]] + state['messages'][-6:]

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_to_send,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        if stop_reason == "stop":
            state['final_answer'] = message.content
            state['messages'].append({
                "role": "assistant",
                "content": message.content
            })
            print(f"✅ Agent finished!")

        elif stop_reason == "tool_calls":
            state['messages'].append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if tool_name == "search_pdf":
                    result = search_pdf(arguments["query"])
                elif tool_name == "search_web":
                    result = search_web(arguments["query"])
                elif tool_name == "calculate":
                    result = calculate(arguments["expression"])
                else:
                    result = "Tool not found"

                state['messages'].append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

    except Exception as e:
        print(f"⚠️ Error: {e}")
        # On error — ask without tools
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_to_send
        )
        state['final_answer'] = response.choices[0].message.content
        print(f"✅ Answered without tools!")

    state['iteration'] += 1
    return state


# ================================
# 🔀 DECISION
# ================================

def should_continue(state: AgentState) -> str:
    if state['final_answer'] or state['iteration'] >= 10:
        return "done"
    return "continue"

# ================================
# 🗺️ BUILD GRAPH
# ================================

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "agent",
        "done": END
    }
)

app = graph.compile()

# ================================
# 🚀 RUN THE ULTIMATE AGENT
# ================================

def run_ultimate_agent(task: str):
    print(f"\n🎯 Task: {task}")
    print("=" * 60)

    # Step 1 — Search PDF
    print("\n📄 Step 1: Searching PDF...")
    pdf_result = search_pdf(task)

    # Step 2 — Search Web
    print("\n🔍 Step 2: Searching Web...")
    web_result = search_web(task)

    # Step 3 — LLM combines everything
    print("\n🧠 Step 3: Combining results...")
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Combine the information from the PDF and web search to give a comprehensive answer."
            },
            {
                "role": "user",
                "content": f"""
Task: {task}

📄 PDF Document says:
{pdf_result}

🔍 Web Search found:
{web_result}

Please combine both sources and give a comprehensive answer.
"""
            }
        ]
    )

    final_answer = response.choices[0].message.content

    print("\n" + "=" * 60)
    print("🏆 FINAL ANSWER:")
    print("=" * 60)
    print(final_answer)
    return final_answer

# ================================
# 📄 LOAD YOUR PDF
# ================================

load_pdf("Function discussion.pdf")  # ← your PDF name here

# ================================
# 🧪 TEST IT!
# ================================

run_ultimate_agent("What hardware components are mentioned in my document?")
