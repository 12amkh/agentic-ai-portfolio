# 🤖 Agentic AI Portfolio
### Built by [12amkh](https://github.com/12amkh)

A collection of AI Agents built from scratch — from a simple LLM call to a full Ultimate Agent.
Every project is fully understood, not just copied. Built in Python using free APIs only.

---

## 🗂️ Projects

### 01 — First LLM Call
> A simple call to an LLM using the Groq API.
- **Tech:** Groq API, LLaMA 3.3
- **Concepts:** LLM basics, API calls

---

### 02 — Memory Agent
> A conversational agent that remembers the full chat history.
- **Tech:** Groq API
- **Concepts:** Short-term memory, conversation history

---

### 03 — ReAct Agent with Tools
> An autonomous agent that decides which tool to use to complete a task.
- **Tech:** Groq API, Function Calling
- **Concepts:** Tool use, ReAct pattern, autonomous decision making

---

### 04 — RAG Agent
> An agent that answers questions from documents using semantic search.
- **Tech:** ChromaDB, Sentence Transformers, Groq API
- **Concepts:** RAG, Vector DB, semantic search, embeddings

---

### 05 — RAG Agent with Real PDF
> Reads any real PDF and answers questions from it intelligently.
- **Tech:** ChromaDB, Sentence Transformers, PyPDF, Groq API
- **Concepts:** PDF chunking, RAG pipeline, context retrieval

---

### 06 — Multi-Agent System (CrewAI)
> Three specialized agents (Researcher, Analyst, Writer) collaborate to produce a full report.
- **Tech:** CrewAI, Groq API
- **Concepts:** Multi-agent collaboration, task delegation, sequential processing

---

### 07 — LangGraph Agent
> A graph-based agent with loops and conditional decisions — reviews its own output and retries if needed.
- **Tech:** LangGraph, LangChain, Groq API
- **Concepts:** State machines, conditional edges, self-review loops

---

### 08 — Real Web Search Agent
> An agent that searches the real internet to answer questions with live data.
- **Tech:** Groq API, Tavily Search
- **Concepts:** Real-time search, tool use, ReAct loop

---

### 09 — Ultimate Agent 🏆
> The final boss — combines RAG, real web search, PDF reading, and LangGraph into one powerful agent.
- **Tech:** Groq API, Tavily, ChromaDB, Sentence Transformers, PyPDF, LangGraph
- **Concepts:** RAG + Web Search + Tools + Graph flow + Context management

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Groq API](https://groq.com) | LLM inference (LLaMA 3.3) — Free |
| [ChromaDB](https://www.trychroma.com) | Local vector database — Free |
| [Sentence Transformers](https://www.sbert.net) | Local embeddings — Free |
| [CrewAI](https://www.crewai.com) | Multi-agent framework |
| [LangGraph](https://langchain-ai.github.io/langgraph) | Graph-based agent flows |
| [Tavily](https://tavily.com) | Real-time web search — Free tier |
| [PyPDF](https://pypdf.readthedocs.io) | PDF reading & parsing |

> 💡 All APIs used have a free tier — no paid subscriptions needed!

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/12amkh/agentic-ai-portfolio.git
cd agentic-ai-portfolio
```

### 2. Install dependencies
```bash
pip install groq chromadb sentence-transformers pypdf crewai langgraph langchain-groq tavily-python python-dotenv
```

### 3. Create `.env` file
```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### 4. Run any project
```bash
cd 03_react_agent
python agent.py
```

---

## 📚 Concepts Covered

- How LLMs work (Transformers, Attention, Training, RLHF)
- Hallucination, Bias, and how Agents solve them
- Tool use and the ReAct pattern
- RAG pipelines with Vector Databases
- Multi-Agent collaboration with CrewAI
- Graph-based agents with loops using LangGraph
- Connecting agents to the real internet with Tavily
- Secure API key management with `.env`

---

## 🗺️ Learning Roadmap

```
LLM Call → Memory → Tools → RAG → PDF → Multi-Agent → LangGraph → Web Search → Ultimate Agent
```

Each project builds on the previous one — no shortcuts, full understanding. 💪

---

## 📬 Contact

- GitHub: [@12amkh](https://github.com/12amkh)

---

> Built from scratch using free tools only.
> Every line of code is understood, not just copied. 💪
