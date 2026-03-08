# 🤖 Agentic AI Portfolio
### Built by [12amkh](https://github.com/12amkh)

A collection of AI Agents built from scratch — from a simple LLM call to a full Multi-Agent system.
Each project is a step forward in understanding and building real-world Agentic AI.

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
> Three specialized agents (Researcher, Analyst, Writer) work together to produce a full report.
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

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Groq API](https://groq.com) | LLM inference (LLaMA 3.3) |
| [ChromaDB](https://www.trychroma.com) | Local vector database |
| [Sentence Transformers](https://www.sbert.net) | Free local embeddings |
| [CrewAI](https://www.crewai.com) | Multi-agent framework |
| [LangGraph](https://langchain-ai.github.io/langgraph) | Graph-based agent flows |
| [Tavily](https://tavily.com) | Real-time web search |
| [PyPDF](https://pypdf.readthedocs.io) | PDF reading & parsing |

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

## 📚 What I Learned

- How LLMs work under the hood (Transformers, Attention, Training)
- How to give LLMs tools and let them decide autonomously
- How to build RAG pipelines with Vector Databases
- How to build Multi-Agent systems with CrewAI
- How to build graph-based agents with loops using LangGraph
- How to connect agents to the real internet with Tavily

---

## 📬 Contact

- GitHub: [@12amkh](https://github.com/12amkh)

---

> Built from scratch — no shortcuts, full understanding. 💪
