from dotenv import load_dotenv
import json
import asyncio

from livekit import agents, api
from livekit.agents import AgentSession, Agent, RoomInputOptions, RunContext, function_tool
from livekit.agents import get_job_context
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant. You can handle both inbound and outbound calls.")
        
    @function_tool
    async def end_call(self, ctx: RunContext):
        """Called when the user wants to end the call"""
        # let the agent finish speaking
        current_speech = ctx.session.current_speech
        if current_speech:
            await current_speech.wait_for_playout()

        await hangup_call()
        
    @function_tool
    async def detected_answering_machine(self):
        """Call this tool if you have detected a voicemail system, AFTER hearing the voicemail greeting"""
        await self.session.generate_reply(
            instructions="Leave a voicemail message letting the user know you'll call back later."
        )
        await asyncio.sleep(0.5)  # Add a natural gap to the end of the voicemail message
        await hangup_call()


async def hangup_call():
    ctx = get_job_context()
    if ctx is None:
        # Not running in a job context
        return
    
    await ctx.api.room.delete_room(
        api.DeleteRoomRequest(
            room=ctx.room.name,
        )
    )

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVCTelephony(),
        ),
    )
    
    # Check if this is an outbound call by looking for phone_number in metadata
    is_outbound_call = False
    phone_number = None
    
    if ctx.job and ctx.job.metadata:
        try:
            dial_info = json.loads(ctx.job.metadata)
            phone_number = dial_info.get("phone_number")
            if phone_number:
                is_outbound_call = True
                print(f"Outbound call to {phone_number} connected")
        except json.JSONDecodeError:
            print("Failed to parse job metadata as JSON")
    
    # Only greet first for inbound calls
    # For outbound calls, wait for the user to speak first
    if not is_outbound_call:
        await session.generate_reply(
            instructions="Greet the user and offer your assistance."
        )


# if __name__ == "__main__":
#     agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,

        # agent_name is required for explicit dispatch
        agent_name="my-telephony-agent"
    ))