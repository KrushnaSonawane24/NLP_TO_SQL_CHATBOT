"""
Simple FastAPI Backend for React Frontend (Original Version Only)
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

from nl2sql.agent import answer_question
from nl2sql.config import load_settings_custom
from nl2sql.db import PostgresDB, DatabaseError
from nl2sql.llm_client import LLMError

load_dotenv()

app = FastAPI(
    title="NL2SQL API",
    description="Natural Language to SQL Query API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = load_settings_custom()  # Using DATABASE_URL_CUSTOMER


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


@app.post('/api/query', response_model=QueryResponse)
async def query(request: QueryRequest):
    """NL2SQL endpoint"""
    try:
        if not request.question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Question is required'
            )
        
        db = PostgresDB(settings.database_url)
        
        response = answer_question(
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


# Alias for langchain endpoint (same implementation for now)
@app.post('/api/langchain/query', response_model=QueryResponse)
async def query_langchain(request: QueryRequest):
    """LangChain endpoint (uses same backend for now)"""
    return await query(request)


@app.get('/api/health', response_model=HealthResponse)
async def health():
    """Health check"""
    return HealthResponse(
        status='healthy',
        provider=settings.provider,
        model=settings.model
    )


if __name__ == '__main__':
    import uvicorn
    
    print("🚀 NL2SQL FastAPI Backend Started!")
    print(f"📍 Running on: http://localhost:8000")
    print(f"🤖 Provider: {settings.provider}")
    print(f"📦 Model: {settings.model}")
    print("\n✅ Endpoints:")
    print("  POST /api/query")
    print("  POST /api/langchain/query")
    print("  GET  /api/health")
    print("  GET  /docs - Interactive API Documentation")
    print("\n🌐 Frontend: Open frontend/index.html in browser")
    print("=" * 50)
    
    uvicorn.run("api_custom:app", host="0.0.0.0", port=8000, reload=True)
