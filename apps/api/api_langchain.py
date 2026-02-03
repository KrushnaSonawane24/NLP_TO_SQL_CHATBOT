"""
FastAPI Backend for React Frontend
Provides REST API endpoints for both original and LangChain NL2SQL implementations
Converted from Flask to FastAPI
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os
from dotenv import load_dotenv

# Add src to path (go up 2 levels to project root, then to src)
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(PROJECT_ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from nl2sql.agent import answer_question as answer_question_original
from nl2sql.config import load_settings_langchain
from nl2sql.db import PostgresDB, DatabaseError
from nl2sql.llm_client import LLMError

# Try importing LangChain (optional)
try:
    from nl2sql_langchain.agent_lc import LangChainAgent, NL2SQLError as LangChainError
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    LangChainAgent = None
    LangChainError = Exception

load_dotenv()

app = FastAPI(
    title="NL2SQL API with LangChain",
    description="Natural Language to SQL Query API with LangChain Support",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = load_settings_langchain()  # Using DATABASE_URL_GIS (PostGIS)

# LangChain agent will be initialized on first request
_langchain_agent_cache = None


def get_langchain_agent():
    """Lazy initialize LangChain agent"""
    global _langchain_agent_cache
    if _langchain_agent_cache is None:
        if not LANGCHAIN_AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="LangChain is not available"
            )
        _langchain_agent_cache = LangChainAgent(
            provider=settings.provider,
            api_key=settings.api_key,
            model=settings.model,
            sql_mode="write_full",
            max_sql_statements=settings.max_sql_statements
        )
    return _langchain_agent_cache


# Pydantic models for request/response
class ChatMessage(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, Any]]] = []


class QueryResponse(BaseModel):
    answer: str
    sql: Optional[str] = None
    results: Optional[Any] = None
    kind: str


class HealthResponse(BaseModel):
    status: str
    provider: str
    model: str
    langchain_enabled: bool


@app.post('/api/query', response_model=QueryResponse)
async def query_original(request: QueryRequest):
    """Original NL2SQL endpoint"""
    try:
        if not request.question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Question is required'
            )
        
        db = PostgresDB(settings.database_url)
        
        response = answer_question_original(
            provider=settings.provider,
            api_key=settings.api_key,
            model=settings.model,
            db=db,
            question=request.question,
            chat_history=request.chat_history,
            statement_timeout_ms=settings.statement_timeout_ms,
            max_rows=settings.max_rows,
            sql_mode="write_full",
            execute=True,
            memory_user_turns=settings.memory_user_turns,
            max_sql_statements=settings.max_sql_statements
        )
        
        # Format results
        results_data = None
        if response.results:
            results_data = [r.rows for r in response.results]
            # Flatten if single result
            if len(results_data) == 1:
                results_data = results_data[0]
        
        return QueryResponse(
            answer=response.answer,
            sql=response.sql,
            results=results_data,
            kind=response.kind
        )
        
    except (LLMError, DatabaseError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal server error: {str(e)}'
        )


@app.post('/api/langchain/query', response_model=QueryResponse)
async def query_langchain(request: QueryRequest):
    """LangChain NL2SQL endpoint"""
    try:
        agent = get_langchain_agent()
        
        if not request.question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Question is required'
            )
        
        db = PostgresDB(settings.database_url)
        
        # Add to memory
        agent.add_to_memory("user", request.question)
        
        response = agent.answer_question(
            db=db,
            question=request.question,
            execute=True,
            statement_timeout_ms=settings.statement_timeout_ms,
            max_rows=settings.max_rows
        )
        
        # Add response to memory
        agent.add_to_memory("assistant", response.answer)
        
        # Format results
        results_data = None
        if response.results:
            results_data = [r.rows for r in response.results]
            if len(results_data) == 1:
                results_data = results_data[0]
        
        return QueryResponse(
            answer=response.answer,
            sql=response.sql,
            results=results_data,
            kind=response.kind
        )
        
    except (DatabaseError, LangChainError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal server error: {str(e)}'
        )


@app.get('/api/health', response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status='healthy',
        provider=settings.provider,
        model=settings.model,
        langchain_enabled=LANGCHAIN_AVAILABLE
    )


if __name__ == '__main__':
    import uvicorn
    
    print("🚀 NL2SQL FastAPI Backend Started!")
    print(f"📍 Running on: http://localhost:8000")
    print(f"🤖 Provider: {settings.provider}")
    print(f"📦 Model: {settings.model}")
    print(f"🔗 LangChain: {'Enabled ✅' if LANGCHAIN_AVAILABLE else 'Disabled ❌'}")
    print("\n✅ API Endpoints:")
    print("  POST /api/query - Original NL2SQL")
    print("  POST /api/langchain/query - LangChain NL2SQL")
    print("  GET  /api/health - Health check")
    print("  GET  /docs - Interactive API Documentation (Swagger UI)")
    print("  GET  /redoc - Alternative API Documentation (ReDoc)")
    print("\n🌐 Frontend: Open frontend/index.html in browser")
    print("=" * 60)
    
    uvicorn.run("api_langchain:app", host="0.0.0.0", port=8001, reload=True)
