# 🔍 CUSTOM FLOW - Complete Detailed Explanation

## 📋 Table of Contents
1. [Overview - Kya Hai Custom Flow?](#overview)
2. [Complete File Structure](#file-structure)
3. [Step-by-Step Flow of Execution](#execution-flow)
4. [Detailed File Breakdown](#file-breakdown)
5. [How to Make Changes](#how-to-make-changes)
6. [Common Modifications Guide](#modifications)
7. [Troubleshooting](#troubleshooting)

---

## 1️⃣ Overview - Kya Hai Custom Flow? {#overview}

### **Custom Flow Kya Hai?**

Custom Flow ek **manually built**, **fully controlled** Natural Language to SQL system hai jo:
- Direct PostgreSQL queries generate karta hai
- **Customer database** se connect hota hai
- Aapka full control hai har step par
- LangChain ka use NAHI karta

### **Kab Use Karein?**
- Simple, direct SQL queries ke liye
- Fast responses chahiye
- Customer data analysis
- Full control chahiye query generation par

### **Access Points:**
- **Streamlit UI:** http://localhost:8501
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 2️⃣ Complete File Structure {#file-structure}

```
Custom Flow Files:
│
├── 📁 apps/
│   ├── 📁 streamlit/
│   │   └── 📄 app_custom.py          ← Streamlit Web UI (Port 8501)
│   │
│   └── 📁 api/
│       └── 📄 api_custom.py          ← FastAPI Backend (Port 8000)
│
├── 📁 src/
│   └── 📁 nl2sql/
│       ├── 📄 config.py              ← Configuration & Database URL
│       ├── 📄 agent.py               ← Main NL2SQL Logic (BRAIN)
│       ├── 📄 llm_client.py          ← LLM Communication (Groq/Gemini)
│       ├── 📄 db.py                  ← Database Connection & Queries
│       └── 📄 sql_safety.py          ← SQL Validation & Safety
│
└── 📄 .env                            ← Environment Variables
```

---

## 3️⃣ Step-by-Step Flow of Execution {#execution-flow}

### **🎯 User Query → SQL → Result (Complete Journey)**

```
┌─────────────────────────────────────────────────────────────┐
│  USER: "Show top 10 customers by revenue"                  │
└─────────────────────────────────────────────────────────────┘
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 1: User Opens Streamlit App                     ║
    ║  File: apps/streamlit/app_custom.py                   ║
    ║  Port: http://localhost:8501                          ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 2: Load Configuration                           ║
    ║  File: src/nl2sql/config.py                          ║
    ║  Function: load_settings_custom()                     ║
    ║  Action: Reads DATABASE_URL_CUSTOMER from .env        ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 3: Connect to Database                          ║
    ║  File: src/nl2sql/db.py                              ║
    ║  Class: PostgresDB                                    ║
    ║  Action: Connect to customer database                 ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 4: Fetch Database Schema                        ║
    ║  File: src/nl2sql/db.py                              ║
    ║  Function: fetch_schema()                             ║
    ║  Returns: All table & column information              ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 5: Generate SQL Plan                            ║
    ║  File: src/nl2sql/agent.py                           ║
    ║  Function: generate_plan()                            ║
    ║  Action:                                              ║
    ║  1. Takes user question                               ║
    ║  2. Takes database schema                             ║
    ║  3. Sends to LLM (Groq/Gemini)                       ║
    ║  4. Gets back JSON response with SQL                  ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 6: LLM Generates SQL                            ║
    ║  File: src/nl2sql/llm_client.py                      ║
    ║  Function: chat_completion()                          ║
    ║  LLM Response:                                        ║
    ║  {                                                    ║
    ║    "kind": "sql",                                     ║
    ║    "message": "Query returned 10 rows",               ║
    ║    "sql": "SELECT * FROM customers                    ║
    ║            ORDER BY revenue DESC LIMIT 10;"           ║
    ║  }                                                    ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 7: Validate SQL Safety                          ║
    ║  File: src/nl2sql/sql_safety.py                      ║
    ║  Function: validate_sql()                             ║
    ║  Checks:                                              ║
    ║  - Is SQL safe to run?                                ║
    ║  - No DROP/TRUNCATE commands?                         ║
    ║  - UPDATE/DELETE has WHERE clause?                    ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 8: Execute SQL                                  ║
    ║  File: src/nl2sql/db.py                              ║
    ║  Function: execute_sql()                              ║
    ║  Action: Runs SQL on customer database                ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
    ╔═══════════════════════════════════════════════════════╗
    ║  STEP 9: Return Results to UI                         ║
    ║  File: apps/streamlit/app_custom.py                   ║
    ║  Display: Shows results in table format               ║
    ╚═══════════════════════════════════════════════════════╝
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  USER SEES: Table with top 10 customers                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4️⃣ Detailed File Breakdown {#file-breakdown}

### 📄 **File 1: `.env` (Environment Variables)**

**Location:** Root directory  
**Purpose:** Configuration storage

```bash
# Database - CUSTOM FLOW USES THIS
DATABASE_URL_CUSTOMER=postgresql://postgres:pass123@localhost:5432/customer

# LLM API Keys
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional Settings
NL2SQL_STATEMENT_TIMEOUT_MS=8000
NL2SQL_MAX_ROWS=200
```

**Yahan changes karo for:**
- ✅ Database URL change
- ✅ API key change
- ✅ Model change
- ✅ Timeout/limit settings

---

### 📄 **File 2: `src/nl2sql/config.py`**

**Purpose:** Configuration loading

**Key Function:**
```python
def load_settings_custom() -> Settings:
    """Load settings for CUSTOM flow - uses DATABASE_URL_CUSTOMER"""
    settings = load_settings()
    customer_db_url = os.getenv("DATABASE_URL_CUSTOMER", "").strip()
    if customer_db_url:
        return Settings(
            provider=settings.provider,
            api_key=settings.api_key,
            model=settings.model,
            database_url=customer_db_url,  # ← USES CUSTOMER DB
            # ... other settings
        )
    return settings
```

**Ye file kya karti hai:**
1. `.env` file se `DATABASE_URL_CUSTOMER` read karti hai
2. API keys load karti hai
3. Settings object return karti hai

**Yahan changes karo for:**
- ✅ New environment variables add karne ke liye
- ✅ Default values change karne ke liye

---

### 📄 **File 3: `src/nl2sql/db.py`**

**Purpose:** Database operations

**Key Class: `PostgresDB`**
```python
class PostgresDB:
    def __init__(self, database_url: str):
        self._database_url = database_url
    
    def fetch_schema(self) -> str:
        """Fetch all tables and columns"""
        # Returns schema like:
        # TABLE customers
        #   - id (integer)
        #   - name (text)
        #   - revenue (numeric)
    
    def execute_sql(self, sql: str) -> QueryResult:
        """Execute SQL and return results"""
```

**Ye file kya karti hai:**
1. Database se connect karti hai
2. Schema fetch karti hai (tables, columns)
3. SQL execute karti hai
4. Results return karti hai

**Yahan changes karo for:**
- ✅ Schema fetching logic change
- ✅ PostGIS detection (already added!)
- ✅ Custom query timeout

---

### 📄 **File 4: `src/nl2sql/agent.py` (🧠 BRAIN)**

**Purpose:** Main NL2SQL logic - SABSE IMPORTANT FILE!

**Key Functions:**

#### **4.1 generate_plan()**
```python
def generate_plan(
    provider: str,
    api_key: str,
    model: str,
    schema_text: str,      # Database schema
    question: str,         # User question
    chat_history: list,    # Previous conversation
    sql_mode: str,         # read_only/write_full
) -> dict:
    """
    LLM ko question bhejta hai aur SQL plan return karta hai
    
    Process:
    1. System prompt banata hai (instructions for LLM)
    2. User question + schema bhejta hai
    3. LLM se JSON response milta hai:
       {
         "kind": "sql",
         "message": "...",
         "sql": "SELECT ..."
       }
    """
```

**System Prompt (Enterprise + PostGIS) - LINE 358-447:**
```python
system = (
    "You are an ENTERPRISE-GRADE PostgreSQL + PostGIS database assistant.\n"
    "This is for an IT consulting and geospatial analytics company.\n"
    # ... PostgreSQL features
    # ... PostGIS features  
    # ... Multi-language support
)
```

**Yahan changes karo for:**
- ✅ LLM instructions modify karne ke liye
- ✅ New SQL patterns add karne ke liye
- ✅ Custom rules add karne ke liye

#### **4.2 answer_question()**
```python
def answer_question(
    provider: str,
    api_key: str,
    model: str,
    db: PostgresDB,
    question: str,
    execute: bool = True,  # Execute SQL or just generate?
) -> NL2SQLResponse:
    """
    Complete question answering flow
    
    Steps:
    1. fetch_schema() - Get database structure
    2. generate_plan() - Get SQL from LLM
    3. validate_sql() - Check if SQL is safe
    4. execute_sql() - Run SQL (if execute=True)
    5. Return results
    """
```

**Yahan changes karo for:**
- ✅ Execution flow modify karne ke liye
- ✅ Custom validation add karne ke liye
- ✅ Response format change karne ke liye

---

### 📄 **File 5: `src/nl2sql/llm_client.py`**

**Purpose:** LLM communication

**Key Function:**
```python
def chat_completion(
    provider: str,           # "groq" or "gemini"
    api_key: str,
    model: str,
    messages: list,          # [system prompt, user message]
    temperature: float,
    max_tokens: int,
) -> str:
    """
    LLM ko call karta hai aur response return karta hai
    
    Supports:
    - Groq (llama models)
    - Gemini (Google)
    """
```

**Yahan changes karo for:**
- ✅ New LLM provider add karne ke liye
- ✅ Temperature/tokens modify karne ke liye
- ✅ Retry logic add karne ke liye

---

### 📄 **File 6: `src/nl2sql/sql_safety.py`**

**Purpose:** SQL validation & safety

**Key Functions:**

```python
def validate_sql(sql: str, sql_mode: str) -> list[str]:
    """
    SQL safety check karta hai
    
    Checks:
    - No DROP/TRUNCATE
    - UPDATE/DELETE has WHERE clause
    - Only allowed operations
    """

def classify_statement(sql: str) -> str:
    """Returns: select, insert, update, delete, etc."""

def apply_limit(sql: str, max_rows: int) -> str:
    """Add LIMIT to SELECT queries"""
```

**Yahan changes karo for:**
- ✅ Custom validation rules
- ✅ New SQL patterns allow/block karne ke liye
- ✅ Safety restrictions modify karne ke liye

---

### 📄 **File 7: `apps/streamlit/app_custom.py`**

**Purpose:** Web UI (Streamlit)

**Key Sections:**

#### **7.1 Configuration (Lines 1-20)**
```python
# Path setup
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC)

# Import custom settings
from nl2sql.config import load_settings_custom  # ← CUSTOM DB
settings = load_settings_custom()  # ← Uses DATABASE_URL_CUSTOMER
```

#### **7.2 Streamlit UI Setup (Lines 22-218)**
```python
st.set_page_config(title="NL2SQL", page_icon="⚙️")
# CSS styling (ChatGPT-inspired dark theme)
st.title("NL → SQL Assistant")
```

#### **7.3 Sidebar Configuration (Lines 222-254)**
```python
with st.sidebar:
    st.subheader("Database Configuration")
    database_url = st.text_input("PostgreSQL URL", value=settings.database_url)
    
    st.subheader("LLM Configuration")
    # Shows provider, model info
    
    st.subheader("Query Safety")
    sql_mode = st.selectbox("Mode", ["read_only", "write_full"])
```

#### **7.4 Chat Interface (Lines 317-397)**
```python
prompt = st.chat_input("Ask a question...")

if prompt:
    # 1. Add to chat history
    # 2. Call answer_question()
    # 3. Display SQL
    # 4. Execute if safe (for READ queries)
    # 5. Ask confirmation for WRITE queries
```

**Yahan changes karo for:**
- ✅ UI styling modify karne ke liye
- ✅ Sidebar options add/remove karne ke liye
- ✅ Chat display format change karne ke liye
- ✅ Custom buttons/features add karne ke liye

---

### 📄 **File 8: `apps/api/api_custom.py`**

**Purpose:** REST API (FastAPI)

**Key Sections:**

#### **8.1 API Setup (Lines 1-43)**
```python
app = FastAPI(title="NL2SQL API")

# CORS for frontend
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Load custom settings
settings = load_settings_custom()  # ← Uses DATABASE_URL_CUSTOMER
```

#### **8.2 Request/Response Models (Lines 45-66)**
```python
class QueryRequest(BaseModel):
    question: str
    chat_history: list = []

class QueryResponse(BaseModel):
    answer: str
    sql: str
    results: Any
    kind: str
```

#### **8.3 API Endpoints (Lines 68-135)**

**POST /api/query**
```python
@app.post('/api/query')
async def query(request: QueryRequest):
    """
    Main NL2SQL endpoint
    
    Input: {"question": "Show top customers"}
    Output: {
        "answer": "Query returned 10 rows",
        "sql": "SELECT * FROM ...",
        "results": [...],
        "kind": "sql"
    }
    """
```

**GET /api/health**
```python
@app.get('/api/health')
async def health():
    """Health check endpoint"""
```

**Yahan changes karo for:**
- ✅ New API endpoints add karne ke liye
- ✅ Request/response format change karne ke liye
- ✅ Custom middleware add karne ke liye
- ✅ Authentication add karne ke liye

---

## 5️⃣ How to Make Changes {#how-to-make-changes}

### **🎨 UI Changes (Streamlit)**

**File:** `apps/streamlit/app_custom.py`

**Change Title:**
```python
# Line 209
st.title("Your New Title")
```

**Change Colors:**
```python
# Lines 30-206 (CSS section)
background-color: #030303;  # Change to your color
```

**Add New Sidebar Option:**
```python
# After Line 254
with st.sidebar:
    new_option = st.selectbox("New Option", ["A", "B", "C"])
```

---

### **🔧 API Changes (FastAPI)**

**File:** `apps/api/api_custom.py`

**Add New Endpoint:**
```python
# After Line 135
@app.get('/api/custom-endpoint')
async def custom_endpoint():
    return {"message": "Hello"}
```

**Change Response Format:**
```python
# Modify QueryResponse class (Line 55)
class QueryResponse(BaseModel):
    # Add new fields here
    custom_field: str = ""
```

---

### **🧠 LLM Behavior Changes**

**File:** `src/nl2sql/agent.py`

**Modify System Prompt:**
```python
# Line 358-447
system = (
    "You are an ENTERPRISE-GRADE PostgreSQL assistant.\n"
    # Add your custom instructions here
    "NEW INSTRUCTION: Always add comments to SQL.\n"
)
```

**Change Temperature/Tokens:**
```python
# Line 412-413
temperature=0.2,  # Lower = more focused, Higher = more creative
max_tokens=1000,  # Increase for longer responses
```

---

### **🔒 Safety Rules Changes**

**File:** `src/nl2sql/sql_safety.py`

**Allow New SQL Commands:**
```python
# Modify validation logic
def validate_sql(sql: str, sql_mode: str):
    # Add custom rules here
```

**Change SQL Modes:**
```python
# In agent.py, modify mode_rules (Lines 335-356)
# Add custom mode like "analytics_only"
```

---

### **🗄️ Database Changes**

**File:** `.env`

**Change Database:**
```bash
# Change this line
DATABASE_URL_CUSTOMER=postgresql://user:pass@host:port/new_database
```

**File:** `src/nl2sql/db.py`

**Modify Schema Fetching:**
```python
# Line 30-78 (fetch_schema function)
# Add custom schema logic
```

---

## 6️⃣ Common Modifications Guide {#modifications}

### **✅ Change 1: Add Hindi Language Support**

**Already Done!** System prompt me Hindi/Hinglish support hai.

**Test:**
```
Query: "Top 10 customers dikhao"
```

---

### **✅ Change 2: Add Custom SQL Functions**

**File:** `src/nl2sql/agent.py`

```python
# In system prompt (Line 380-390)
"- Custom functions: calculate_revenue(customer_id)\n"
```

---

### **✅ Change 3: Add Query Caching**

**File:** `apps/api/api_custom.py`

```python
# Add caching
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(question: str):
    # Your logic
```

---

### **✅ Change 4: Add Logging**

**File:** `src/nl2sql/agent.py`

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In answer_question
logger.info(f"Question: {question}")
logger.info(f"Generated SQL: {sql}")
```

---

## 7️⃣ Troubleshooting {#troubleshooting}

### **❌ Error: ModuleNotFoundError: No module named 'nl2sql'**

**Solution:**
```python
# Check path in app files (Line 9-18)
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC)
```

---

### **❌ Error: Cannot connect to database**

**Check:**
1. `.env` me correct URL hai?
2. Database server chal raha hai?
3. Credentials correct hain?

**Test Connection:**
```python
# Run this in Python
import psycopg2
conn = psycopg2.connect("postgresql://postgres:pass123@localhost:5432/customer")
print("Connected!")
```

---

### **❌ Error: LLM not responding**

**Check:**
1. `.env` me API key correct hai?
2. Internet connection hai?
3. Rate limits exceeded nahi ho gaye?

**Test API Key:**
```bash
# For Groq
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

### **❌ Error: SQL validation failing**

**File:** `src/nl2sql/sql_safety.py`

**Temporarily disable for testing:**
```python
# Comment out validation
# raise UnsafeSQLError("...")
```

---

## 📊 Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  CUSTOM FLOW - QUICK REFERENCE                          │
├─────────────────────────────────────────────────────────┤
│  🌐 UI:        http://localhost:8501                    │
│  🔌 API:       http://localhost:8000                    │
│  📚 Docs:      http://localhost:8000/docs               │
│  💾 Database:  customer (DATABASE_URL_CUSTOMER)         │
├─────────────────────────────────────────────────────────┤
│  FILES TO MODIFY:                                       │
│  ├─ UI Changes:      apps/streamlit/app_custom.py      │
│  ├─ API Changes:     apps/api/api_custom.py            │
│  ├─ LLM Behavior:    src/nl2sql/agent.py               │
│  ├─ DB Logic:        src/nl2sql/db.py                  │
│  ├─ SQL Safety:      src/nl2sql/sql_safety.py          │
│  └─ Configuration:   .env                               │
└─────────────────────────────────────────────────────────┘
```

---

**💡 Pro Tip:** Har change ke baad service restart karo for changes to take effect!

**Next:** LangChain Flow ki detailed explanation alag message me!
