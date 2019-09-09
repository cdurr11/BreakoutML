from flask import Flask
from flask_socketio import send, emit, SocketIO
import time
import os, sys
from game import Game
import numpy as np

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from tensorflow.keras import backend as K

app = Flask(__name__)

socketio = SocketIO(app)

FRAMES_PER_SECOND = 60

def init():
    global model, graph, session
    model = Sequential()
    model.add(Dense(32, activation='relu', input_shape=(6,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(2, activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    model.load_weights("training_1/cp.ckpt")
    model._make_predict_function()
    session = K.get_session()
    graph = tf.get_default_graph()
    # graph.finalize()



@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('init')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    global game
    game = Game(2,10,60)
    # game.initialize_blocks()
    game_blocks = game.get_blocks()
    pixel_width = game.get_pixel_width()
    pixel_height = game.get_pixel_height()
    block_size = game.get_block_size()
    #rows are do not include wall blocks
    # paddle_width = game.get_paddle().get_width()
    rows = game.get_rows()
    columns = game.get_columns()

    json_blocks = [block.get_position() for block in game_blocks]

    socketio.emit('init_resp', {
        'rows' : rows,
        'columns' : columns,
        'pixel_width' : pixel_width,
        'pixel_height' : pixel_height,
        'block_size': block_size,
        # 'blocks' : json_blocks,
    });
    handle_play()

# @socketio.on('start_play')
def handle_play(method=['GET', 'POST']):
    # global graph
    # print("json: ", json)
    # time.sleep(1)
    while True:
        time.sleep(1/FRAMES_PER_SECOND)
        #do game logic here, emit updated things, repeat
        if NEURAL_NET_PLAY:
            with graph.as_default():
                with session.as_default():
                    state = np.array([game.get_game_state_vector()])
                    print(model.summary())
                    # prediction = model.predict(state)
                    prediction = np.argmax(model.predict(state))
                    # print(prediction)
                    if prediction == 0:
                        game.time_step({'left' : True, 'right' : False})
                    else:
                        game.time_step({'left' : False, 'right' : True})

        else:
            game.time_step(json)

        socketio.emit('step',
        {
            'paddle' : game.get_paddle_location_json(),
            'blocks': game.get_blocks_json(),
            'ball' : game.get_ball_location_json(),
            'game_state':game.get_game_state(),
            'score' : game.get_score(),
        });



@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    while (True):
        socketio.emit('my response', {'blocks': [[True],[True],[True]]})
        time.sleep(1/FRAMES_PER_SECOND)

if __name__ == '__main__':
    print("running python server")
    global NEURAL_NET_PLAY
    NEURAL_NET_PLAY = True
    if NEURAL_NET_PLAY:
        init()
    socketio.run(app, debug=False)


    # app.run()
