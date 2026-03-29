import socketio
from fastapi import FastAPI
import uvicorn

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
sio_app = socketio.ASGIApp(sio, app)

# --- STATE MANAGEMENT ---
# A set to keep track of all connected session IDs (sids).
# If you add usernames later, you can change this to a dictionary: {sid: "username"}
active_users = set()

async def broadcast_user_update():
    """Helper function to broadcast the current user list to the room"""
    await sio.emit('user_update', {
        'count': len(active_users),
        'users': list(active_users) # Sets aren't JSON serializable, so convert to list
    }, room="global_room")


@app.get("/")
def home():
    return "Relay Server Running"

@sio.event
async def connect(sid, environ):
    print(f"User Connected: {sid}")
    await sio.enter_room(sid, "global_room")