# LangChain NL2SQL Implementation Guide

## 🎯 What's Different?

This is a **LangChain-powered version** of the NL2SQL chatbot with the following improvements:

### ✨ Key Features

1. **Built-in Memory** 🧠
   - LangChain automatically manages conversation history
   - Bot remembers last 10 messages (configurable)
   - No manual history formatting needed

2. **Structured Prompts** 📝
   - Uses `ChatPromptTemplate` instead of f-strings
   - `MessagesPlaceholder` for automatic memory injection
   - Cleaner, more maintainable prompt logic

3. **Provider Abstraction** 🔌
   - Built-in support for Gemini (`ChatGoogleGenerativeAI`)
   - Built-in support for Groq (`ChatGroq`)
   - No manual HTTP requests needed

4. **Chain Architecture** ⛓️
   - LangChain's LCEL (LangChain Expression Language)
   - `prompt | llm | json_parser` pipeline
   - Easier to extend with additional steps

## 📁 File Structure

```
cursor_sql_chatbot/
├── app.py                         # Original version
├── app_langchain.py               # 🆕 LangChain version
├── requirements.txt               # Original dependencies
├── requirements_langchain.txt     # 🆕 LangChain dependencies
└── src/
    ├── nl2sql/                    # Original implementation
    │   ├── agent.py
    │   ├── llm_client.py
    │   ├── db.py
    │   ├── sql_safety.py
    │   └── config.py
    └── nl2sql_langchain/          # 🆕 LangChain implementation
        ├── __init__.py
        └── agent_lc.py            # Main LangChain agent
```

## 🚀 How to Run

### Step 1: Install LangChain Dependencies
```bash
pip install -r requirements_langchain.txt
```

### Step 2: Run the LangChain App
```bash
streamlit run app_langchain.py
```

## 🔍 Code Comparison

### Memory Management

**Original (Manual):**
```python
def _format_short_history(chat_history, max_user_prompts=5):
    pairs = []
    for t in reversed(chat_history):
        # Manual parsing and formatting
        ...
    return "\n".join(lines)
```

**LangChain (Automatic):**
```python
# Memory is handled by MessagesPlaceholder
# Just add messages to agent
agent.add_to_memory("user", "Show me users")
agent.add_to_memory("assistant", "Here are the users...")
```

### LLM Calling

**Original (HTTP Requests):**
```python
import requests
resp = requests.post(
    f"https://generativelanguage.googleapis.com/...",
    headers=headers,
    data=json.dumps(payload)
)
```

**LangChain (Built-in):**
```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
result = chain.invoke({"question": question})
```

### Prompt Construction

**Original (f-strings):**
```python
system = (
    f"You are a SQL expert...\n"
    f"Schema: {schema_text}\n"
    f"Rules: {mode_rules}\n"
)
```

**LangChain (Templates):**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a SQL expert..."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "SCHEMA:\n{schema}\n\nQUESTION:\n{question}"),
])
```

## 📊 Comparison Table

| Feature | Original | LangChain |
|---------|----------|-----------|
| **Lines of Code** | ~800 | ~350 |
| **Dependencies** | 4 | 8 |
| **Memory Management** | Manual | Automatic |
| **Prompt Engineering** | f-strings | Templates |
| **LLM Integration** | HTTP requests | Built-in classes |
| **Extensibility** | Medium | High |
| **Learning Curve** | Low | Medium |
| **Control** | Full | Abstracted |
| **Debugging** | Easier | Harder |

## 🎓 When to Use Which?

### Use Original (`app.py`) When:
- ✅ You want full control over every API call
- ✅ You want minimal dependencies
- ✅ Performance is critical (less abstraction overhead)
- ✅ You're learning how LLMs work from scratch

### Use LangChain (`app_langchain.py`) When:
- ✅ You want built-in memory management
- ✅ You plan to add more complex features (agents, tools, RAG)
- ✅ You want rapid prototyping
- ✅ You're building a production-ready app with many LLM features

## 💡 Memory Feature Demo

Try this conversation:

**You:** "Show me all users"  
**Bot:** Returns SQL + Data

**You:** "Now show only users from Mumbai"  
**Bot:** Remembers you're talking about "users" table 🧠

**You:** "What was the first query I asked?"  
**Bot:** Can reference previous conversation! 🎯

## 🔒 Safety Note

Both versions use the **same safety layer** (`sql_safety.py`). LangChain doesn't compromise security - all SQL is still validated before execution.

## 🐛 Troubleshooting

**Error: `langchain not found`**
```bash
pip install -r requirements_langchain.txt
```

**Error: `Import error nl2sql`**
- Make sure you're running from project root
- Check that `src/` is in Python path

**Memory not working?**
- Verify agent is initialized in session state
- Check that `add_to_memory()` is called after each response

## 📚 Learn More

- [LangChain Docs](https://python.langchain.com/)
- [Chat Models](https://python.langchain.com/docs/modules/model_io/chat/)
- [Memory](https://python.langchain.com/docs/modules/memory/)
- [Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/)
