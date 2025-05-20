#!/bin/bash
# LiveKit Agent Deployment Script
# This script deploys the latest code to the EC2 instance and restarts the service

# Exit on any error
set -e

# Configuration
SSH_KEY="~/.ssh/livekit-agent.pem"
EC2_HOST="ubuntu@ec2-3-101-146-37.us-west-1.compute.amazonaws.com"
REPO_PATH="/home/ubuntu/dev/github.com/mmcc007/ai-voice"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting deployment of LiveKit Agent...${NC}"

# Check if SSH key exists
if [ ! -f $(eval echo $SSH_KEY) ]; then
    echo -e "${RED}Error: SSH key not found at $SSH_KEY${NC}"
    exit 1
fi

# Deploy commands to run on the remote server
echo -e "${YELLOW}Connecting to EC2 instance...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" << 'EOF'
    # Print current directory and hostname for verification
    echo "Connected to $(hostname) as $(whoami)"
    
    # Navigate to the repository
    cd /home/ubuntu/dev/github.com/mmcc007/ai-voice
    
    # Check if we're in the right directory
    if [ ! -d .git ]; then
        echo "Error: Not a git repository"
        exit 1
    fi
    
    # Save the current commit hash for comparison
    OLD_COMMIT=$(git rev-parse HEAD)
    
    echo "Pulling latest changes from git repository..."
    git fetch
    git pull
    
    # Get the new commit hash
    NEW_COMMIT=$(git rev-parse HEAD)
    
    if [ "$OLD_COMMIT" == "$NEW_COMMIT" ]; then
        echo "No changes to deploy. Already at the latest version."
    else
        echo "Changes detected. Showing git log:"
        git log --oneline $OLD_COMMIT..$NEW_COMMIT
        
        # Check if virtual environment exists and activate it
        if [ -d .venv ]; then
            echo "Activating virtual environment and installing dependencies..."
            source .venv/bin/activate
            pip install -r requirements.txt
        else
            echo "Warning: Virtual environment not found at .venv"
        fi
        
        # FastAPI service is already set up, no need to recreate the service file
        echo "FastAPI server service is already configured..."

        # Reload systemd to recognize the new service
        sudo systemctl daemon-reload

        # Enable the FastAPI service to start on boot
        sudo systemctl enable fastapi-server.service
        
        # Restart the services
        echo "Restarting LiveKit agent service..."
        sudo systemctl restart livekit-agent
        
        echo "Starting FastAPI server service..."
        sudo systemctl restart fastapi-server
        
        # Check service status
        echo "LiveKit agent service status:"
        sudo systemctl status livekit-agent --no-pager
        
        echo "FastAPI server service status:"
        sudo systemctl status fastapi-server --no-pager
    fi
EOF

# Check if the SSH command was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Deployment completed successfully!${NC}"
else
    echo -e "${RED}Deployment failed!${NC}"
    exit 1
fi
