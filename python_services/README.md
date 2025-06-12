# Chief-of-Flow Python Services

AI-powered personal task management and scheduling system built with FastAPI, SQLAlchemy, and OpenAI integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database (Supabase recommended)
- OpenAI API key (optional, fallback mode available)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd python_services
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Start the development server:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Test the API:**
   ```bash
   python test_api.py
   ```

## 📁 Project Structure

```
python_services/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/          # API route handlers
│   │   │   ├── tasks.py        # Task CRUD + AI features
│   │   │   ├── projects.py     # Project management
│   │   │   ├── schedule.py     # Schedule management
│   │   │   ├── ai.py          # AI chat & personality
│   │   │   └── health.py      # Health checks
│   │   └── api.py             # Router configuration
│   ├── core/
│   │   ├── config.py          # Pydantic settings
│   │   └── database.py        # SQLAlchemy + Supabase
│   ├── models/
│   │   └── database.py        # SQLAlchemy models
│   ├── schemas/
│   │   └── task.py           # Pydantic schemas
│   ├── services/
│   │   ├── ai_service.py      # OpenAI integration
│   │   ├── task_service.py    # Task business logic
│   │   ├── project_service.py # Project management
│   │   └── schedule_service.py # Scheduling logic
│   └── main.py               # FastAPI application
├── requirements.txt          # Python dependencies
├── test_setup.py            # Import validation
├── test_api.py              # API endpoint tests
└── .env.example             # Environment template
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Application
APP_NAME=Chief-of-Flow
DEBUG=true
SECRET_KEY=your-secret-key

# Database (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
DATABASE_URL=postgresql+asyncpg://postgres:password@db.your-project.supabase.co:5432/postgres

# AI (Optional)
OPENAI_API_KEY=your-openai-api-key

# API
CORS_ORIGINS=["http://localhost:3000"]
```

### Fallback Mode

The system gracefully handles missing API keys:
- **Without OpenAI**: AI features use fallback responses
- **Without Supabase**: Database operations will fail gracefully
- **Development Mode**: All imports and basic functionality work without external services

## 📚 API Documentation

### Base URLs
- **Development**: `http://localhost:8000`
- **API v1**: `http://localhost:8000/api/v1`
- **Docs**: `http://localhost:8000/docs` (when DEBUG=true)

### Core Endpoints

#### Health & Status
```bash
GET /                          # Service info
GET /health                    # Health check (requires DB)
GET /api/v1/health/           # Basic health check
GET /api/v1/health/detailed   # Detailed health check
```

#### AI Features
```bash
GET  /api/v1/ai/status                    # AI capabilities
POST /api/v1/ai/chat                      # Chat with AI
POST /api/v1/ai/personality-assessment    # Personality assessment
```

#### Tasks
```bash
GET    /api/v1/tasks/                     # List tasks
POST   /api/v1/tasks/                     # Create task
GET    /api/v1/tasks/{task_id}           # Get task
PUT    /api/v1/tasks/{task_id}           # Update task
DELETE /api/v1/tasks/{task_id}           # Delete task
POST   /api/v1/tasks/from-text           # Create from natural language
POST   /api/v1/tasks/search              # Semantic search
```

#### Projects
```bash
GET    /api/v1/projects/                  # List projects
POST   /api/v1/projects/                  # Create project
GET    /api/v1/projects/{project_id}     # Get project
PUT    /api/v1/projects/{project_id}     # Update project
DELETE /api/v1/projects/{project_id}     # Delete project
```

#### Schedule
```bash
GET  /api/v1/schedule/                    # Get daily schedule
POST /api/v1/schedule/                    # Create schedule entry
```

## 🧠 AI Features

### Natural Language Task Creation
```bash
POST /api/v1/tasks/from-text
{
  "input_text": "I need to buy groceries tomorrow before 5pm",
  "context": {"project": "personal"}
}
```

### Semantic Task Search
```bash
POST /api/v1/tasks/search
{
  "query": "grocery shopping",
  "limit": 10,
  "similarity_threshold": 0.7
}
```

### AI Chat with Personality
```bash
POST /api/v1/ai/chat
{
  "message": "How should I prioritize my tasks today?",
  "context": {"mood": "stressed"}
}
```

## 🗄️ Database Models

### Core Tables
- **`projects`**: Project organization and importance
- **`tasks`**: Tasks with AI embeddings and dependencies
- **`daily_schedule`**: Time-blocked schedule entries
- **`schedule_template`**: Weekly routine templates
- **`user_llm_instructions`**: Custom AI instructions
- **`user_personality_profile`**: Personality assessment data

### Key Features
- **Row Level Security (RLS)**: All tables secured by user_id
- **Vector Search**: pgvector embeddings for semantic search
- **Async Operations**: Full async/await support
- **Type Safety**: Pydantic schemas for validation

## 🧪 Testing

### Run All Tests
```bash
# Test imports and configuration
python test_setup.py

# Test API endpoints
python test_api.py

# Test with real database (requires .env setup)
python -c "from app.main import app; print('✅ Full app import successful')"
```

### Expected Test Results
- ✅ All imports successful
- ✅ Configuration loaded
- ✅ Pydantic validation working
- ✅ API endpoints responding
- ✅ AI fallback functionality working

## 🚀 Development

### Adding New Endpoints
1. Create route handler in `app/api/v1/endpoints/`
2. Add Pydantic schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Add tests to `test_api.py`

### Database Changes
1. Update SQLAlchemy models in `app/models/database.py`
2. Create Alembic migration (if using migrations)
3. Update Pydantic schemas
4. Test with `test_setup.py`

### AI Integration
1. Extend `AIService` in `app/services/ai_service.py`
2. Add fallback functionality for development
3. Update AI status endpoint
4. Test with and without OpenAI API key

## 🔒 Security

### Authentication
- TODO: Implement JWT authentication
- Current: Mock user ID for development

### Database Security
- ✅ Row Level Security (RLS) enabled
- ✅ User isolation enforced
- ✅ SQL injection protection via SQLAlchemy

### API Security
- ✅ CORS configured
- ✅ Input validation via Pydantic
- ✅ Error handling without data leaks

## 📈 Performance

### Optimizations
- ✅ Async database operations
- ✅ Connection pooling
- ✅ Structured logging
- ✅ Lazy loading for Supabase clients

### Monitoring
- Health check endpoints
- Structured JSON logging
- Error tracking and metrics

## 🚢 Deployment

### Production Checklist
- [ ] Set `DEBUG=false`
- [ ] Configure production database
- [ ] Set secure `SECRET_KEY`
- [ ] Configure CORS origins
- [ ] Set up monitoring
- [ ] Enable HTTPS

### Docker Deployment
```dockerfile
# TODO: Add Dockerfile for containerized deployment
```

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass
5. Use structured logging

## 📄 License

This project is part of the Chief-of-Flow personal task management system. 