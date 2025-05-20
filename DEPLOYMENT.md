# Deployment Guide for AI Voice Calling System

This guide explains how to deploy both the LiveKit agent and the FastAPI server to your EC2 instance.

## Prerequisites

- EC2 instance running Ubuntu
- SSH access to the EC2 instance
- Git repository set up on the EC2 instance
- `.env` file with LiveKit credentials on the EC2 instance

## Deployment Process

### Automatic Deployment

The included `deploy.sh` script will:

1. Connect to your EC2 instance
2. Pull the latest code from the git repository
3. Set up the virtual environment and install dependencies
4. Create and configure systemd services for both:
   - The LiveKit agent
   - The FastAPI server
5. Restart both services
6. Show the status of both services

To deploy, simply run:

```bash
./deploy.sh
```

### Manual Deployment

If you prefer to deploy manually, follow these steps:

1. SSH into your EC2 instance
2. Navigate to the repository directory
3. Pull the latest changes: `git pull`
4. Activate the virtual environment: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create systemd service files for both services
7. Reload systemd: `sudo systemctl daemon-reload`
8. Enable and start the services:
   ```bash
   sudo systemctl enable livekit-agent
   sudo systemctl enable fastapi-server
   sudo systemctl restart livekit-agent
   sudo systemctl restart fastapi-server
   ```

## Accessing the Services

### FastAPI Server

The FastAPI server will be running on port 8000. To access it:

- **Local testing**: http://localhost:8000
- **EC2 instance**: http://your-ec2-public-ip:8000

Make sure your EC2 security group allows inbound traffic on port 8000.

### API Documentation

Once deployed, you can access the auto-generated API documentation:

- Swagger UI: http://your-ec2-public-ip:8000/docs
- ReDoc: http://your-ec2-public-ip:8000/redoc

## Deploying the Next.js Frontend

For the web frontend, you have two options:

### Option 1: Deploy to Vercel (Recommended)

1. Push your code to a GitHub repository
2. Import the project in Vercel
3. Set the `API_URL` environment variable to point to your EC2 instance:
   ```
   API_URL=http://your-ec2-public-ip:8000
   ```
4. Deploy

### Option 2: Deploy to the Same EC2 Instance

You can also deploy the Next.js app to the same EC2 instance:

1. Install Node.js on the EC2 instance
2. Navigate to the web-app directory
3. Install dependencies: `npm install`
4. Build the app: `npm run build`
5. Create a systemd service for the Next.js app
6. Configure a reverse proxy (e.g., Nginx) to serve both the API and the web app

## Troubleshooting

### Checking Service Logs

To check the logs for either service:

```bash
# LiveKit agent logs
sudo journalctl -u livekit-agent -f

# FastAPI server logs
sudo journalctl -u fastapi-server -f
```

### Common Issues

- **Port already in use**: Make sure no other service is using port 8000
- **Permission denied**: Check that the user running the service has the necessary permissions
- **Environment variables missing**: Verify that the `.env` file exists and contains all required variables
