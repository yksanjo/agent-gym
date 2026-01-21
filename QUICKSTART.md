# Agent Gym Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Clone the Repository
```bash
git clone https://github.com/yksanjo/agent-gym.git
cd agent-gym
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Start Development Servers
```bash
# Option A: Using Docker Compose (recommended)
docker-compose up -d

# Option B: Manual start
# Backend:
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Frontend (in another terminal):
cd frontend
npm run dev
```

### 4. Access the Application
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## 📋 What's Included

### Backend Features
- ✅ Agent management API
- ✅ Feedback collection system
- ✅ Database models for A/B testing
- ✅ Fine-tuning pipeline structure
- ✅ Synthetic data generation framework

### Frontend Foundation
- ✅ Next.js 14 with TypeScript
- ✅ Tailwind CSS for styling
- ✅ React Query for data fetching
- ✅ Radix UI components

### Development Tools
- ✅ Docker Compose configuration
- ✅ PostgreSQL + Redis services
- ✅ Python virtual environment
- ✅ Setup script for easy onboarding

## 🧪 Try It Out

### Example API Calls
```bash
# Check API status
curl http://localhost:8000/health

# List agents
curl http://localhost:8000/api/v1/agents/

# Create a new agent
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Agent", "description": "Example agent"}'
```

### Run Example Integration
```bash
cd examples
python basic_integration.py
```

## 🛠️ Development Workflow

### 1. Make Changes
```bash
# Create a new branch
git checkout -b feature/your-feature

# Make your changes
# Test locally
```

### 2. Run Tests
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

### 3. Commit and Push
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature
```

## 📁 Project Structure
```
agent-gym/
├── backend/           # FastAPI backend
│   ├── api/          # API endpoints
│   ├── models.py     # Database models
│   ├── schemas.py    # Pydantic schemas
│   └── main.py       # Application entry
├── frontend/         # Next.js frontend
│   ├── package.json  # Dependencies
│   └── ...           # React components
├── examples/         # Integration examples
├── docs/             # Documentation
└── docker-compose.yml # Service orchestration
```

## 🔧 Configuration

### Environment Variables
Create `.env` file in `backend/`:
```bash
DATABASE_URL=postgresql://agentgym:agentgym123@localhost:5432/agentgym
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-key
```

### Database Setup
```bash
# Initialize database
cd backend
source venv/bin/activate
python -c "from database import init_db; init_db()"
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Or use different ports
   uvicorn main:app --port 8001 --reload
   ```

2. **Database connection failed**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps postgres
   
   # Restart services
   docker-compose restart postgres redis
   ```

3. **Python package issues**
   ```bash
   cd backend
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Getting Help
- Check the [documentation](README.md)
- Review [implementation guide](IMPLEMENTATION_GUIDE.md)
- Look at [example code](examples/basic_integration.py)

## 🎯 Next Steps

### For Developers
1. Implement missing API endpoints
2. Build frontend components
3. Add authentication system
4. Create comprehensive tests

### For Users
1. Integrate with your existing agents
2. Set up feedback collection
3. Configure A/B testing
4. Monitor agent performance

## 📞 Support
- GitHub Issues: [Report bugs](https://github.com/yksanjo/agent-gym/issues)
- Documentation: [Read docs](README.md)
- Examples: [See integration examples](examples/)

---

**Happy coding!** 🚀

*Last updated: 2024-01-20*