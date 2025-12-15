#!/bin/bash

# Stop script for Cold Case IA Application

echo "🛑 Stopping Cold Case IA Application..."

docker-compose down

echo ""
echo "✅ Application stopped successfully"
echo ""
echo "To remove all data (including ChromaDB):"
echo "  docker-compose down -v"
echo ""
