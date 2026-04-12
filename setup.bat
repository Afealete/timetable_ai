@echo off
REM AI TIMETABLE RESOURCE ALLOCATOR - Windows Setup Script
REM This script helps set up the development environment on Windows

echo 🚀 AI TIMETABLE RESOURCE ALLOCATOR - Setup Script
echo =================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18.0 or higher.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Setup backend
echo.
echo 🔧 Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

echo ✅ Backend setup complete!

REM Setup frontend
echo.
echo 🎨 Setting up frontend...
cd ../frontend

REM Install dependencies
echo 📥 Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!

REM Create necessary directories
echo.
echo 📁 Creating necessary directories...
cd ..
if not exist "backend\uploads" mkdir backend\uploads
if not exist "backend\exports" mkdir backend\exports

echo.
echo 🎉 Setup complete!
echo.
echo To run the application:
echo 1. Start backend: cd backend ^& venv\Scripts\activate.bat ^& python app.py
echo 2. Start frontend: cd frontend ^& npm run dev
echo.
echo Then open http://localhost:5173 in your browser
echo.
echo Happy scheduling! 📅

pause