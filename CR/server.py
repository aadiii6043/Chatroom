from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

admin_sid = None  # Admin's socket ID
users = {}  # Approved users
pending_users = {}  # Users waiting for approval

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_user')
def handle_new_user(username):
    global admin_sid
    if not admin_sid:
        # First user becomes the admin
        admin_sid = request.sid
        users[request.sid] = username
        emit("message", f"👑 {username} is now the admin!", broadcast=True)
        emit("admin", room=admin_sid)  # Notify this user they are the admin
    else:
        pending_users[request.sid] = username
        emit("message", f"🔶 {username} is requesting to join (ID: {request.sid})", room=admin_sid)
        emit("pending_users", pending_users, room=admin_sid)  # Send the updated list to the admin

@socketio.on('approve_user')
def approve_user(user_sid):
    if request.sid == admin_sid and user_sid in pending_users:
        username = pending_users.pop(user_sid)
        users[user_sid] = username
        emit("message", f"✅ {username} has been approved!", broadcast=True)
        emit("approved", room=user_sid)  # Enable chat for approved user
        emit("pending_users", pending_users, room=admin_sid)  # Update pending list for admin
    else:
        emit("message", "❌ Approval failed.", room=request.sid)

@socketio.on('message')
def handle_message(msg):
    if request.sid in users:
        username = users[request.sid]
        send(f"{username}: {msg}", broadcast=True)
    else:
        emit("message", "❌ You are not approved yet!", room=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        username = users.pop(request.sid)
        emit("message", f"🔴 {username} has left the chat!", broadcast=True)
    elif request.sid in pending_users:
        pending_users.pop(request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)