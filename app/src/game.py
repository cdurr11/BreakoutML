import os, sys
# sys.path.append(os.path.abspath('.'))
from bodies import Block, Paddle
from vector import Vector
# from .bodies import Block

class Game():
    def __init__(self, rows, columns, block_size, height = 10):
        self.rows = rows
        self.columns = columns
        self.block_size = block_size
        self.height = height
        self.pixel_height = height * block_size
        #in pixels
        self.pixel_width = ( columns + 2 ) * block_size
        self.blocks = self.initialize_blocks()
        self.paddle = Paddle((self.pixel_width//2 - block_size//2, self.pixel_height - block_size), block_size)
        # self.ball = Ball()

    #retuns a 1D array of all blocks in the game (hard/soft) and the order that
    #they will be added to the game
    def initialize_blocks(self):
        #position for blocks is the top left corner
        #all blocks in the game will be kept in a single array

        #should have at least 4 gap between the blocks and the bottom of the game
        assert self.height > self.rows + 4
        self.blocks = []
        for r in range(self.height):
            for c in range(self.columns + 2):
                if (c == 0 or c == self.columns + 1 or r == 0):
                    self.blocks.append(Block(((self.block_size*(c)), self.block_size*(r)), "HARD", self.block_size))
                else:
                    if (r <= self.rows):
                        self.blocks.append(Block(((self.block_size*(c)), self.block_size*(r)), "SOFT", self.block_size))

    #gets all of the blocks in the game as a 1D array
    def get_blocks(self):
        return self.blocks

    #TODO figure out the scale for paddle speed
    def update_paddle(self, keys):
        if (keys['left'] and keys['right']):
            pass

        # horizontal_paddle_speed = 5;
        elif (keys['left']):
            self.paddle.update_position(Vector(-10,0))
            paddle_pos_x = self.paddle.get_position()[0]
            #inside the left wall
            if paddle_pos_x < self.block_size:
                translation_vector = Vector(self.block_size - paddle_pos_x, 0)
                self.paddle.update_position(translation_vector)

        elif (keys['right']):
            self.paddle.update_position(Vector(10,0))
            paddle_pos_x = self.paddle.get_position()[0]
            #inside right wall
            if paddle_pos_x + self.paddle.get_width() > self.get_pixel_width() - self.block_size:
                right_overlap = (paddle_pos_x + self.paddle.get_width()) - (self.get_pixel_width() - self.block_size)
                translation_vector = Vector(-right_overlap, 0)
                self.paddle.update_position(translation_vector)

    #keys {'left' : Boolean, 'right' : Boolean}
    def time_step(self, keys):
        self.update_paddle(keys)
        #first update paddle
        #cancel each other out


    #returns true if the ball and the other_body intersect else false
    def check_ball_intersections(ball, other_body):
        pass

    def check_paddle_intersections(paddle, wall_block):
        pass

    #returns a new vector that results from the resolved collision
    def resolve_collision(ball, other_body):
        pass

    #returns true if the ball is in bounds, false otherwise
    def check_ball_in_bounds(ball):
        pass

    def get_pixel_width(self):
        return self.pixel_width

    def get_pixel_height(self):
        return self.pixel_height

    def get_block_size(self):
        return self.block_size

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def get_paddle(self):
        return self.paddle

    def get_paddle_location_json(self):
        return {'x' : self.paddle.get_position()[0],
                'y' : self.paddle.get_position()[1],
                'width' : self.paddle.get_width()}


    def get_blocks_json(self):
        final_blocks_json = []
        for block in self.blocks:
            final_blocks_json.append(
                {
                    'x': block.get_position()[0],
                    'y': block.get_position()[1],
                    'type' : block.get_type(),
                    'exists' : block.get_exists(),
                })

        return final_blocks_json;
