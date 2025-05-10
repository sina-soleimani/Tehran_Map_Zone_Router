# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from routes import init_routes  # Import init_routes to bind events to SocketIO
import logging
logger = logging.getLogger(__name__)
from errors import ErrorMessage


app = Flask(__name__)
socketio = SocketIO(app)

# Initialize routes after creating the app and socketio instance
init_routes(socketio)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error( ErrorMessage.HOME_route_ERROR)
        return ErrorMessage.HOME_route_ERROR , 500

if __name__ == '__main__':
    socketio.run(app, debug=True)
