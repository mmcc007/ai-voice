# AI Voice Calling Web Application

A Next.js web application for making outbound calls using LiveKit AI voice agents.

## Features

- Clean, modern UI built with Next.js and Tailwind CSS
- Simple form for making outbound calls
- Integration with the FastAPI backend

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API server running (see parent directory)

### Installation

1. Install dependencies:

```bash
npm install
```

2. Create a `.env.local` file with the following content:

```
# API URL (default: http://localhost:8000)
API_URL=http://localhost:8000
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
npm run build
npm run start
```

## Deployment

This application can be deployed to Vercel:

1. Push your code to a Git repository
2. Import the project in Vercel
3. Set the environment variables
4. Deploy

## API Integration

The web app communicates with the FastAPI backend server to make outbound calls. Make sure the API server is running before using the web application.
