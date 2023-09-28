from app import app, socketio
from app.routes import *

if __name__ == '__main__':
    socketio.run(app, debug=True)