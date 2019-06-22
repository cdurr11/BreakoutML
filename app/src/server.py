from flask import Flask
from flask_socketio import send, emit, SocketIO
import time
app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    while (True):
        # socketio.emit('my response', "hello")
        time.sleep(1/60)
    # print('received my event: ' + str(json))
    # print("sending")



if __name__ == '__main__':
    print("running python server")
    socketio.run(app, debug=False)

    # app.run()
