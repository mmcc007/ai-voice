#!/bin/bash

# Run the API server and Next.js app in development mode

# Function to clean up processes when script is terminated
cleanup() {
  echo "Shutting down services..."
  kill $API_PID $NEXT_PID 2>/dev/null
  exit 0
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

# Check if Python dependencies are installed
if ! command -v uvicorn &> /dev/null; then
  echo "Installing Python dependencies..."
  pip install -r requirements.txt
fi

# Check if Node.js dependencies are installed
if [ ! -d "web-app/node_modules" ]; then
  echo "Installing Node.js dependencies..."
  cd web-app && npm install && cd ..
fi

# Start the FastAPI server
echo "Starting API server on http://localhost:8000..."
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Wait a bit for the API server to start
sleep 2

# Start the Next.js app
echo "Starting Next.js app on http://localhost:3000..."
cd web-app && npm run dev &
NEXT_PID=$!

echo "Development environment is running!"
echo "API server: http://localhost:8000"
echo "Next.js app: http://localhost:3000"
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $API_PID $NEXT_PID
