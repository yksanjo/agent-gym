#!/bin/bash

# Agent Gym Setup Script
# This script sets up the development environment for Agent Gym

set -e

echo "🚀 Setting up Agent Gym development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p backend/logs
mkdir -p frontend/public
mkdir -p data/postgres
mkdir -p data/redis

# Set up backend
echo "🐍 Setting up Python backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file..."
    cat > .env << EOF
# Application
APP_NAME=Agent Gym
ENVIRONMENT=development
DEBUG=True

# Database
DATABASE_URL=postgresql://agentgym:agentgym123@postgres:5432/agentgym

# Redis
REDIS_URL=redis://redis:6379/0

# Security
JWT_SECRET_KEY=your-secret-key-change-in-production

# API Keys (optional)
OPENAI_API_KEY=
HUGGINGFACE_TOKEN=
EOF
    echo "✅ Created .env file. Please update with your API keys if needed."
fi

cd ..

# Set up frontend
echo "⚛️ Setting up React frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

# Create .env.local file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "🔧 Creating .env.local file..."
    cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Agent Gym
EOF
fi

cd ..

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis

echo "⏳ Waiting for services to be ready..."
sleep 10

# Initialize database
echo "🗄️ Initializing database..."
cd backend
source venv/bin/activate
python -c "
from database import init_db
init_db()
print('✅ Database initialized successfully')
"

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the development servers:"
echo "1. Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker Compose:"
echo "docker-compose up"
echo ""
echo "Access the applications:"
echo "• Backend API: http://localhost:8000"
echo "• API Docs: http://localhost:8000/docs"
echo "• Frontend: http://localhost:3000"
echo ""
echo "To stop everything:"
echo "docker-compose down"