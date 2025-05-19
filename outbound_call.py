#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import argparse
from dotenv import load_dotenv

from livekit import api
from livekit.agents import cli

# Load environment variables
load_dotenv()

async def make_outbound_call(phone_number: str, wait_for_answer: bool = True):
    """
    Make an outbound call to the specified phone number.
    
    Args:
        phone_number: The phone number to call (format: +1XXXXXXXXXX)
        wait_for_answer: Whether to wait until the call is answered before returning
    """
    # Get the trunk ID from environment variables
    trunk_id = os.environ.get("LIVEKIT_OUTBOUND_TRUNK_ID")
    if not trunk_id:
        print("Error: LIVEKIT_OUTBOUND_TRUNK_ID environment variable not set")
        return False
    
    # Generate a unique room name for this call
    import random
    room_name = f"outbound-{''.join(str(random.randint(0, 9)) for _ in range(10))}"
    
    # Create the LiveKit API client
    livekit_api = api.LiveKitAPI()
    
    try:
        print(f"Placing outbound call to {phone_number}...")
        print(f"Using room: {room_name}")
        
        # Create the SIP participant to initiate the call
        participant = await livekit_api.sip.create_sip_participant(api.CreateSIPParticipantRequest(
            # This ensures the participant joins the correct room
            room_name=room_name,
            
            # Use the outbound trunk ID from environment variables
            sip_trunk_id=trunk_id,
            
            # The outbound phone number to dial and identity to use
            sip_call_to=phone_number,
            participant_identity=phone_number,
            
            # This will wait until the call is answered before returning
            wait_until_answered=wait_for_answer,
            
            # Play a dial tone while the call is connecting
            play_dialtone=True,
        ))
        
        print("Call initiated successfully!")
        if wait_for_answer:
            print("Call was answered!")
        
        # Dispatch the agent to handle the call
        print(f"Dispatching agent to room {room_name}...")
        
        # Create agent dispatch request
        dispatch_response = await livekit_api.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                # Use the agent name set in main.py
                agent_name="my-telephony-agent",
                
                # Use the same room name we created for the SIP participant
                room=room_name,
                
                # Pass the phone number in metadata
                metadata=json.dumps({"phone_number": phone_number})
            )
        )
        
        print(f"Agent dispatched successfully!")
        print(f"Call is now active in room: {room_name}")
        return True
        
    except api.TwirpError as e:
        print(f"Error creating SIP participant: {e.message}")
        if hasattr(e, 'metadata'):
            print(f"SIP status: {e.metadata.get('sip_status_code')} {e.metadata.get('sip_status')}")
        return False
    finally:
        await livekit_api.aclose()

async def main():
    parser = argparse.ArgumentParser(description="Make outbound calls with LiveKit")
    parser.add_argument("phone_number", help="Phone number to call (format: +1XXXXXXXXXX)")
    parser.add_argument("--no-wait", action="store_true", help="Don't wait for the call to be answered")
    
    args = parser.parse_args()
    
    # Validate phone number format
    if not args.phone_number.startswith("+"):
        print("Error: Phone number must start with '+' (e.g., +18005551234)")
        sys.exit(1)
    
    success = await make_outbound_call(args.phone_number, not args.no_wait)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
