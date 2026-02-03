# FastAPI Migration Guide

## Overview
This project now supports **both Flask and FastAPI** backends. The FastAPI version provides better performance, automatic API documentation, and modern async support.

## Files

### Flask Backend (Original)
- `api_server_simple.py` - Simple Flask API
- `api_server.py` - Full Flask API with LangChain support
- **Default Port:** 5000

### FastAPI Backend (New) ✨
- `api_server_simple_fastapi.py` - Simple FastAPI API
- `api_server_fastapi.py` - Full FastAPI API with LangChain support
- **Default Port:** 8000

## Quick Start

### 1. Install Dependencies

First, install all required packages:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file is configured:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/database
GEMINI_API_KEY=your_api_key_here
# or
GROQ_API_KEY=your_api_key_here
```

### 3. Run FastAPI Backend (Recommended)

#### Simple Version:
```bash
python api_server_simple_fastapi.py
```

#### Full Version with LangChain:
```bash
python api_server_fastapi.py
```

## API Endpoints

Both Flask and FastAPI backends provide the same endpoints:

### POST /api/query
Main NL2SQL endpoint

**Request:**
```json
{
  "question": "Show me top 10 customers by revenue",
  "chat_history": []
}
```

**Response:**
```json
{
  "answer": "Here are the top 10 customers...",
  "sql": "SELECT * FROM customers...",
  "results": [...],
  "kind": "sql"
}
```

### POST /api/langchain/query
LangChain-powered endpoint (same interface)

### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "provider": "gemini",
  "model": "gemini-pro",
  "langchain_enabled": true
}
```

## FastAPI Advantages

### 1. **Automatic API Documentation** 📚
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. **Better Performance** ⚡
- Async/await support
- Better request handling
- Lower memory footprint

### 3. **Type Safety** 🔒
- Pydantic models for validation
- Automatic request/response validation
- Better error messages

### 4. **Modern Python** 🐍
- Uses Python 3.6+ features
- Type hints throughout
- Better IDE support

## Migration Checklist

If you're migrating from Flask to FastAPI:

- [x] Created FastAPI versions of all Flask files
- [x] Updated `requirements.txt` with FastAPI dependencies
- [x] Maintained same endpoint structure
- [x] Kept backward compatibility
- [ ] Update frontend to use port 8000 (if needed)
- [ ] Test all endpoints
- [ ] Deploy FastAPI version

## Running Both Servers

You can run both Flask and FastAPI simultaneously on different ports:

**Terminal 1 (Flask):**
```bash
python api_server_simple.py  # Runs on port 5000
```

**Terminal 2 (FastAPI):**
```bash
python api_server_simple_fastapi.py  # Runs on port 8000
```

## Frontend Configuration

Update your frontend API URL based on which backend you're using:

**For Flask (port 5000):**
```javascript
const API_URL = 'http://localhost:5000/api';
```

**For FastAPI (port 8000):**
```javascript
const API_URL = 'http://localhost:8000/api';
```

## Testing

### Test Flask Backend:
```bash
curl -X POST http://localhost:5000/api/health
```

### Test FastAPI Backend:
```bash
curl -X GET http://localhost:8000/api/health
```

### Test Query Endpoint:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all tables"}'
```

## Key Differences

| Feature | Flask | FastAPI |
|---------|-------|---------|
| Port | 5000 | 8000 |
| Documentation | Manual | Auto-generated |
| Type Checking | Manual | Automatic (Pydantic) |
| Async Support | Limited | Full |
| Performance | Good | Excellent |
| Learning Curve | Easy | Moderate |

## Troubleshooting

### Port Already in Use
If you get a port error, either:
1. Stop the other server
2. Change the port in the script
3. Use `netstat` to find and kill the process

### Missing Dependencies
```bash
pip install fastapi uvicorn pydantic
```

### CORS Issues
Both backends have CORS enabled for all origins (`*`). In production, specify exact origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    ...
)
```

## Deployment

### FastAPI with Uvicorn
```bash
uvicorn api_server_fastapi:app --host 0.0.0.0 --port 8000
```

### Production Settings
```bash
uvicorn api_server_fastapi:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --no-access-log
```

## Next Steps

1. ✅ Install FastAPI dependencies
2. ✅ Run FastAPI backend
3. 🔄 Update frontend configuration (if needed)
4. 🔄 Test all endpoints
5. 🚀 Deploy to production

## Support

For issues or questions:
1. Check the FastAPI docs: https://fastapi.tiangolo.com/
2. Check existing Flask implementation
3. Review error logs

---

**Recommendation:** Use FastAPI backend for new projects and production deployments. Flask version is kept for backward compatibility.
