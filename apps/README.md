# Apps Directory

This directory contains all **application code** for the NL2SQL PostgreSQL Query Assistant.

---

## 📁 Structure:

```
apps/
├── streamlit/              ← Streamlit web applications
│   ├── app_custom.py      ← Custom NL2SQL implementation
│   └── app_langchain.py   ← LangChain-powered implementation
│
└── api/                    ← FastAPI REST APIs
    ├── api_custom.py      ← Custom NL2SQL API
    └── api_langchain.py   ← LangChain-powered API
```

---

## 🚀 Running Applications:

### Streamlit Apps:

```bash
# Custom implementation
cd apps/streamlit
streamlit run app_custom.py

# LangChain implementation  
cd apps/streamlit
streamlit run app_langchain.py
```

**Access:** http://localhost:8501

### FastAPI APIs:

```bash
# Custom API
cd apps/api
python api_custom.py

# LangChain API
cd apps/api
python api_langchain.py
```

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📚 Application Descriptions:

### `streamlit/app_custom.py`
- **Type:** Streamlit web app
- **Implementation:** Custom NL2SQL agent
- **Memory:** Session-based
- **Best for:** Most users, simple use cases

### `streamlit/app_langchain.py`
- **Type:** Streamlit web app
- **Implementation:** LangChain agent
- **Memory:** Automatic (last 10 messages)
- **Best for:** Advanced users, better context

### `api/api_custom.py`
- **Type:** FastAPI REST API
- **Implementation:** Custom NL2SQL agent
- **Features:** Auto docs, type-safe, fast
- **Best for:** Production deployments

### `api/api_langchain.py`
- **Type:** FastAPI REST API
- **Implementation:** LangChain + Custom agents
- **Features:** Both endpoints available
- **Best for:** Maximum flexibility

---

## ⚙️ Configuration:

All apps use the same `.env` file in project root:

```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
PROVIDER=gemini
GEMINI_API_KEY=your_key_here
MODEL=gemini-1.5-flash
```

---

## 🔗 Dependencies:

Apps use shared code from `../src/`:
- `src/nl2sql/` - Custom implementation
- `src/nl2sql_langchain/` - LangChain integration

---

**Note:** Run apps from their respective directories for proper imports.
