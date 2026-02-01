import socketio
from fastapi import FastAPI
import uvicorn

# Standard Async Server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
sio_app = socketio.ASGIApp(sio, app)

@app.get("/")
def home():
    return "Relay Server Running"

@sio.event
async def connect(sid, environ):
    print(f"✅ User Connected: {sid}")
    # Force everyone into the same global room automatically
    await sio.enter_room(sid, "global_room")
    await sio.emit('status', {'msg': 'New User Connected!'}, room="global_room", skip_sid=sid)

@sio.event
async def disconnect(sid):
    print(f"❌ User Disconnected: {sid}")

# GENERIC RELAY FUNCTION
@sio.event
async def send_video(sid, data):
    # Ignore the 'room' parameter and just send to 'global_room'
    # This guarantees everyone sees it
    await sio.emit('receive_video', data, room="global_room", skip_sid=sid)

@sio.event
async def send_audio(sid, data):
    audio_content = data.get('audio') 
    await sio.emit('receive_audio', {'audio': audio_content}, room="global_room")
