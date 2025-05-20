#!/usr/bin/env python3
import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Import the outbound call function
from outbound_call import make_outbound_call

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="LiveKit Voice AI API")

# Add CORS middleware to allow requests from the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class CallRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number to call (format: +1XXXXXXXXXX)")
    wait_for_answer: bool = Field(True, description="Whether to wait for the call to be answered")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v.startswith('+'):
            raise ValueError("Phone number must start with '+' (e.g., +18005551234)")
        return v

# Define response model
class CallResponse(BaseModel):
    success: bool
    message: str
    room_name: str = None

@app.post("/api/call", response_model=CallResponse)
async def make_call(request: CallRequest):
    """
    Make an outbound call to the specified phone number
    """
    try:
        # Call the existing function from outbound_call.py
        room_name = None
        success = await make_outbound_call(
            phone_number=request.phone_number,
            wait_for_answer=request.wait_for_answer
        )
        
        if success:
            return CallResponse(
                success=True,
                message=f"Call to {request.phone_number} initiated successfully",
                room_name=room_name
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initiate call to {request.phone_number}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
