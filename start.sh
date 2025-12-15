#!/bin/bash

# Start script for Cold Case IA Application
# This script helps you start the application quickly

set -e

echo "🔍 Cold Case IA - Starting Application"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env file and add your ANTHROPIC_API_KEY"
    echo "   Then run this script again."
    echo ""
    echo "Get your API key at: https://console.anthropic.com/"
    exit 1
fi

# Check if API key is set
if grep -q "your_anthropic_api_key_here" .env; then
    echo "⚠️  ANTHROPIC_API_KEY not configured in .env file"
    echo ""
    echo "📝 Please edit .env file and add your real API key:"
    echo "   ANTHROPIC_API_KEY=sk-ant-api03-..."
    echo ""
    echo "Get your API key at: https://console.anthropic.com/"
    exit 1
fi

# Source .env file
export $(cat .env | grep -v '^#' | xargs)

echo "✅ Configuration verified"
echo ""

# Build and start containers
echo "🐋 Building and starting Docker containers..."
echo "   This may take a few minutes on first run..."
echo ""

docker-compose up -d --build

echo ""
echo "✅ Application started successfully!"
echo ""
echo "📍 Access points:"
echo "   - Frontend:  http://localhost:3000"
echo "   - Backend:   http://localhost:8000"
echo "   - API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop application:"
echo "   docker-compose down"
echo ""
echo "⏳ The backend may take a minute to index all documents on first startup."
echo "   You can check progress with: docker-compose logs -f backend"
echo ""
