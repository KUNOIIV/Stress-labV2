# Created my own local multiplayer lobby for QA load testing and breaking local server
# Survives spam, shows real names, works with 10+ tabs instantly

import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Plain white HTML page to enter player name to enter the server
HTML = """
<!DOCTYPE html>
<html>
<head><title>Live Lobby</title></head>
<body>
    <h1>Live Lobby</h1>
    <div id="messages"></div>
    <br>
    <input id="name" placeholder="Your name" autofocus />
    <button onclick="send()">Send / Join</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script>
    <script>
        const socket = io();
        socket.on('message', msg => {
            document.getElementById('messages').innerHTML += <p>${msg}</p>;
        });
        function send() {
            const name = document.getElementById('name').value.trim() || 'Anonymous';
            socket.emit('message', name + ' joined the lobby');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

last_join = {}

@socketio.on('message') # This is to see in terminal when players has entered the server 
# The backend picks up the data and shows player has successfully joined
def handle_message(data):
    ip = request.remote_addr
    now = time.time()

    if ip not in last_join:
        last_join[ip] = now
    elif now - last_join[ip] < 0.1:    # 10 messages per second max per IP
        return                         # Silently drop spam

    last_join[ip] = now
    print('Message:', data)
    emit('message', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)