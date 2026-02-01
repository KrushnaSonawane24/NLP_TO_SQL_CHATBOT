from __future__ import annotations

import os
import sys
import time

import streamlit as st
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from nl2sql.agent import NL2SQLError, answer_question
from nl2sql.config import load_settings
from nl2sql.db import DatabaseError, PostgresDB
from nl2sql.llm_client import LLMError
from nl2sql.sql_safety import SQLMode, classify_statement

load_dotenv()

# Page config with custom theme
st.set_page_config(
    page_title="NL → SQL Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional UI with white and light green theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Main App Styling - Light Green Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%);
        font-family: 'Poppins', 'Inter', sans-serif;
    }
    
    /* Main Container - Pure White */
    .main .block-container {
        padding: 2rem 2rem 3rem;
        max-width: 1200px;
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.8s ease-out;
        border: 1px solid #e0e0e0;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Title Styling - Black Text with Green Accent */
    h1 {
        color: #1b5e20;
        font-weight: 800;
        animation: fadeIn 1s ease-in;
        text-align: center;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Subtitle - Dark Gray Text */
    .subtitle {
        text-align: center;
        color: #424242;
        font-size: 1.15rem;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease-in;
        font-weight: 500;
    }
    
    /* Chat Messages - White Cards with Light Border */
    .stChatMessage {
        background: #ffffff;
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.7rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        animation: messageSlide 0.4s ease-out;
        border: 1px solid #e0e0e0;
    }
    
    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* User message - Light Green Background with Black Text */
    [data-testid="stChatMessageContent"] {
        background: #c8e6c9;
        color: #1b5e20;
        border-radius: 15px;
        padding: 1.2rem;
        border: 1px solid #a5d6a7;
    }
    
    /* Code blocks - Green Border */
    .stCodeBlock {
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        background: #f5f5f5 !important;
    }
    
    /* Sidebar - Light Green Gradient */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #66bb6a 0%, #4caf50 100%);
        padding: 2rem 1rem;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }
    
    .css-1d391kg h2, [data-testid="stSidebar"] h2,
    .css-1d391kg h3, [data-testid="stSidebar"] h3,
    .css-1d391kg p, [data-testid="stSidebar"] p,
    .css-1d391kg label, [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Sidebar inputs - White Background */
    .css-1d391kg .stTextInput input, [data-testid="stSidebar"] .stTextInput input,
    .css-1d391kg .stSelectbox select, [data-testid="stSidebar"] .stSelectbox select,
    .css-1d391kg .stNumberInput input, [data-testid="stSidebar"] .stNumberInput input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 255, 255, 0.5);
        color: #1b5e20;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .css-1d391kg .stTextInput input::placeholder,
    [data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #757575;
    }
    
    /* Buttons - Green Gradient */
    .stButton button {
        background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
    }
    
    /* Dataframes - Clean Table Style */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        animation: tableSlide 0.5s ease-out;
        border: 1px solid #e0e0e0;
    }
    
    @keyframes tableSlide {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Success/Error Messages - Clean Colors */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        animation: pulse 0.5s ease-in;
        font-weight: 500;
    }
    
    .stSuccess {
        background: #66bb6a;
        color: white;
        border: none;
    }
    
    .stError {
        background: #ef5350;
        color: white;
        border: none;
    }
    
    .stWarning {
        background: #ffca28;
        color: #1a1a1a;
        border: none;
    }
    
    .stInfo {
        background: #42a5f5;
        color: white;
        border: none;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Loading Spinner - Green */
    .stSpinner > div {
        border-top-color: #4caf50 !important;
        border-right-color: #66bb6a !important;
    }
    
    /* Expander - Green Header */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
        color: white;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.8rem 1rem;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.5);
        transform: translateY(-1px);
    }
    
    /* Input field - Clean Chat Input */
    .stChatInput {
        border-radius: 25px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* Stats Cards - White Cards with Green Accent */
    .stat-card {
        background: #ffffff;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin: 0.5rem;
        transition: all 0.3s ease;
        border: 2px solid #c8e6c9;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        border-color: #4caf50;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2e7d32;
    }
    
    .stat-label {
        color: #424242;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("<h1>🤖 Natural Language → SQL Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask questions in plain English. Get instant SQL results! ⚡</p>", unsafe_allow_html=True)

settings = load_settings()

# Sidebar with modern styling
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    st.markdown("#### 🔌 Database Connection")
    database_url = st.text_input("DATABASE_URL", value=settings.database_url, type="password")

    st.markdown("#### 🤖 AI Model")
    provider = settings.provider
    api_key = settings.api_key
    model = settings.model
    st.info(f"**Provider:** {provider.upper()}\n\n**Model:** {model}")

    st.markdown("#### 🛡️ Security Settings")
    _sql_mode_options = ["read_only", "write_no_delete", "write_full"]
    _default_sql_mode = st.session_state.get("sql_mode") or "write_full"
    if _default_sql_mode not in _sql_mode_options:
        _default_sql_mode = "write_full"
    sql_mode: SQLMode = st.selectbox(
        "SQL Mode",
        options=_sql_mode_options,
        index=_sql_mode_options.index(_default_sql_mode),
        key="sql_mode",
        help="Read Only: Safe SELECT only | Write Full: CRUD Operations"
    )
    
    statement_timeout_ms = st.number_input(
        "Statement Timeout (ms)", 
        min_value=1000, 
        max_value=60000, 
        value=settings.statement_timeout_ms, 
        step=500
    )
    max_rows = st.number_input(
        "Max Rows", 
        min_value=1, 
        max_value=2000, 
        value=settings.max_rows, 
        step=10
    )
    
    st.markdown("---")
    st.markdown("#### 📊 Stats")
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.get('messages', []))}</div>
        <div class="stat-label">Total Messages</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending" not in st.session_state:
    st.session_state.pending = None
if "sql_mode" not in st.session_state:
    st.session_state.sql_mode = "write_full"

# Display chat history with animations
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sql"):
            with st.expander("📝 Generated SQL", expanded=False):
                st.code(m["sql"], language="sql")
        if m.get("results"):
            for i, r in enumerate(m["results"], start=1):
                if len(m["results"]) > 1:
                    st.caption(f"Statement #{i}")
                if r.get("meta"):
                    st.caption(r["meta"])
                if r.get("rows") is not None:
                    st.dataframe(r["rows"], use_container_width=True)


def _run_pending(db: PostgresDB):
    pending = st.session_state.pending
    if not pending:
        return
    sql = pending["sql"]
    question = pending["question"]
    
    with st.spinner("⚙️ Executing SQL..."):
        time.sleep(0.5)  # Small delay for animation effect
        try:
            resp = answer_question(
                provider=provider,
                api_key=api_key,
                model=model,
                db=db,
                question=question,
                chat_history=st.session_state.messages,
                statement_timeout_ms=int(statement_timeout_ms),
                max_rows=int(max_rows),
                sql_mode=sql_mode,
                execute=True,
                sql_override=sql,
                memory_user_turns=settings.memory_user_turns,
                max_sql_statements=settings.max_sql_statements,
            )
            results_payload = []
            for r in resp.results or []:
                results_payload.append({"rows": r.rows, "meta": f"rowcount: {r.rowcount}"})
            st.session_state.messages.append({
                "role": "assistant", 
                "content": resp.answer, 
                "sql": resp.sql, 
                "results": results_payload
            })
            st.session_state.pending = None
            st.success("✅ Query executed successfully!")
            time.sleep(0.5)
            st.rerun()
        except (NL2SQLError, LLMError, DatabaseError) as e:
            st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {e}"})
            st.session_state.pending = None
            st.rerun()


# Chat input
prompt = st.chat_input("💬 Ask me anything about your database... (e.g., 'Show top 10 users by revenue')")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not database_url:
            st.error("⚠️ Missing DATABASE_URL")
        elif not api_key:
            st.error("⚠️ Missing API key (set GEMINI_API_KEY or GROQ_API_KEY in .env)")
        else:
            with st.spinner("🤔 Thinking..."):
                time.sleep(0.3)  # Animation delay
                try:
                    db = PostgresDB(database_url)
                    resp = answer_question(
                        provider=provider,
                        api_key=api_key,
                        model=model,
                        db=db,
                        question=prompt,
                        chat_history=st.session_state.messages,
                        statement_timeout_ms=int(statement_timeout_ms),
                        max_rows=int(max_rows),
                        sql_mode=sql_mode,
                        execute=False,
                        memory_user_turns=settings.memory_user_turns,
                        max_sql_statements=settings.max_sql_statements,
                    )
                    if resp.kind != "sql" or not resp.sql:
                        st.markdown(resp.answer)
                        st.session_state.messages.append({"role": "assistant", "content": resp.answer})
                    else:
                        with st.expander("📝 Generated SQL", expanded=True):
                            st.code(resp.sql, language="sql")
                        stmts = resp.sql_statements or []
                        all_read = all(classify_statement(s) in ("select", "with") for s in stmts) if stmts else False
                        if all_read:
                            with st.spinner("📊 Fetching data..."):
                                time.sleep(0.3)
                                exec_resp = answer_question(
                                    provider=provider,
                                    api_key=api_key,
                                    model=model,
                                    db=db,
                                    question=prompt,
                                    chat_history=st.session_state.messages,
                                    statement_timeout_ms=int(statement_timeout_ms),
                                    max_rows=int(max_rows),
                                    sql_mode=sql_mode,
                                    execute=True,
                                    sql_override=resp.sql,
                                    memory_user_turns=settings.memory_user_turns,
                                    max_sql_statements=settings.max_sql_statements,
                                )
                                st.markdown(exec_resp.answer)
                                results_payload = []
                                for r in exec_resp.results or []:
                                    results_payload.append({"rows": r.rows, "meta": f"rowcount: {r.rowcount}"})
                                    st.caption(f"📈 Rowcount: {r.rowcount}")
                                    st.dataframe(r.rows, use_container_width=True)
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": exec_resp.answer, 
                                    "sql": exec_resp.sql, 
                                    "results": results_payload
                                })
                        else:
                            if sql_mode == "read_only":
                                st.error("⚠️ Write SQL generated but SQL mode is read_only. Switch to write_full for CRUD.")
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": "Error: write SQL blocked by read_only mode.",
                                    "sql": resp.sql,
                                })
                            else:
                                st.warning("⚠️ This looks like a WRITE query. Review the SQL, then click Execute.")
                                st.session_state.pending = {"sql": resp.sql, "question": prompt}
                                if st.button("🚀 Execute SQL", type="primary"):
                                    _run_pending(db)
                except (NL2SQLError, LLMError, DatabaseError) as e:
                    st.error(f"❌ {str(e)}")
                    st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Display pending SQL in sidebar
if st.session_state.pending and database_url and api_key:
    with st.sidebar:
        st.markdown("---")
        st.markdown("#### ⏳ Pending SQL")
        st.code(st.session_state.pending["sql"], language="sql")
