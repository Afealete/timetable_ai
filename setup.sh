#!/bin/bash

# AI TIMETABLE RESOURCE ALLOCATOR - Setup Script
# This script helps set up the development environment

echo "🚀 AI TIMETABLE RESOURCE ALLOCATOR - Setup Script"
echo "================================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18.0 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup backend
echo ""
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate  # On Windows, this would be: venv\Scripts\activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"

# Setup frontend
echo ""
echo "🎨 Setting up frontend..."
cd ../frontend

# Install dependencies
echo "📥 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
cd ..
mkdir -p backend/uploads
mkdir -p backend/exports

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start backend: cd backend && source venv/bin/activate && python app.py"
echo "2. Start frontend: cd frontend && npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
echo ""
echo "Happy scheduling! 📅"