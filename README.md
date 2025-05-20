# AI Voice Calling System

This project combines LiveKit AI voice agents with a web interface to make outbound calls. The system consists of two main components:

1. **FastAPI Backend**: Exposes the LiveKit outbound calling functionality as a REST API
2. **Next.js Frontend**: Provides a user-friendly web interface for making calls

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Next.js Web    │───▶│  FastAPI        │───▶│  LiveKit        │
│  Application    │◀───│  Server         │◀───│  Voice Agent    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

- Python 3.9+
- Node.js 18+
- LiveKit account with outbound trunk configured
- Environment variables set up in `.env` file

## Getting Started

1. Clone this repository
2. Set up environment variables in `.env` file:

```
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=your_livekit_url
LIVEKIT_OUTBOUND_TRUNK_ID=your_trunk_id
```

3. Run the development environment:

```bash
./run_dev.sh
```

This will:
- Install Python dependencies
- Install Node.js dependencies
- Start the FastAPI server on port 8000
- Start the Next.js app on port 3000

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Components

### FastAPI Backend

The backend server (`api_server.py`) exposes a REST API for making outbound calls:

- `POST /api/call`: Make an outbound call to a phone number
- `GET /api/health`: Health check endpoint

### Next.js Frontend

The frontend web application provides a user interface for making calls:

- Simple form for entering phone numbers
- Option to wait for answer before returning
- Success/error feedback

## Development

For development details, see:
- `api_README.md` for backend information
- `web-app/README.md` for frontend information

## Deployment

### Backend Deployment

The FastAPI server can be deployed to any cloud provider that supports Python applications:

1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment

The Next.js app can be deployed to Vercel:

1. Push your code to a Git repository
2. Import the project in Vercel
3. Set the `API_URL` environment variable to point to your deployed API server
4. Deploy

## License

[MIT](LICENSE)
