import socketio
from fastapi import FastAPI

# Create a Socket.IO server (Asynchronous)
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
sio_app = socketio.ASGIApp(sio, app)

@app.get("/")
def home():
    return "Video Call Relay Server is Running."

# --- WEBSOCKET EVENTS ---

@sio.event
async def connect(sid, environ):
    print(f"User Connected: {sid}")

@sio.event
async def join_room(sid, room_name):
    """User joins a specific 'room' (e.g., 'meeting1')"""
    sio.enter_room(sid, room_name)
    print(f"{sid} joined room: {room_name}")
    await sio.emit('status', {'msg': 'Someone joined!'}, room=room_name, skip_sid=sid)

@sio.event
async def send_video(sid, data):
    """Relay video from Sender to everyone else in the room"""
    room = data['room']
    image = data['image']
    # Send to everyone in the room EXCEPT the sender (skip_sid=sid)
    await sio.emit('receive_video', {'image': image}, room=room, skip_sid=sid)

@sio.event
async def send_audio(sid, data):
    """Relay audio from Sender to everyone else in the room"""
    room = data['room']
    audio = data['audio']
    await sio.emit('receive_audio', {'audio': audio}, room=room, skip_sid=sid)

@sio.event
async def disconnect(sid):
    print(f"User Disconnected: {sid}")