# AI Voice Calling API Server

This FastAPI server exposes a REST API for making outbound calls using LiveKit AI voice agents.

## Features

- RESTful API for making outbound calls
- Integration with LiveKit for voice AI
- CORS support for frontend integration

## Getting Started

### Prerequisites

- Python 3.9+
- LiveKit account with outbound trunk configured
- Environment variables set up (see .env file)

### Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file contains the necessary LiveKit credentials:

```
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=your_livekit_url
LIVEKIT_OUTBOUND_TRUNK_ID=your_trunk_id
```

### Running the API Server

Start the FastAPI server:

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000

### API Documentation

Once the server is running, you can access the auto-generated API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### `POST /api/call`

Make an outbound call to a phone number.

**Request Body:**

```json
{
  "phone_number": "+18005551234",
  "wait_for_answer": true
}
```

**Response:**

```json
{
  "success": true,
  "message": "Call to +18005551234 initiated successfully",
  "room_name": "outbound-1234567890"
}
```

### `GET /api/health`

Health check endpoint.

**Response:**

```json
{
  "status": "ok"
}
```

## Integration with Frontend

This API server is designed to work with the Next.js frontend in the `web-app` directory. The frontend makes requests to this API to initiate outbound calls.
