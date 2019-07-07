from flask import Flask
from flask_socketio import send, emit, SocketIO
import time
import os, sys
from game import Game
app = Flask(__name__)

socketio = SocketIO(app)

FRAMES_PER_SECOND = 60

@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('init')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    global game
    game = Game(2,10,60)
    game.initialize_blocks()
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
    })

@socketio.on('start_play')
def handle_play(json, method=['GET', 'POST']):

    # print("json: ", json)
    # time.sleep(1)
    time.sleep(1/FRAMES_PER_SECOND)
    #do game logic here, emit updated things, repeat
    game.time_step(json)
    socketio.emit('step',
    {
        'paddle' : game.get_paddle_location_json(),
        'blocks': game.get_blocks_json(),
        'ball' : game.get_ball_location_json(),
        'game_state':game.get_game_state(), 
    });



@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    while (True):
        socketio.emit('my response', {'blocks': [[True],[True],[True]]})
        time.sleep(1/FRAMES_PER_SECOND)



if __name__ == '__main__':
    print("running python server")
    socketio.run(app, debug=False)

    # app.run()
