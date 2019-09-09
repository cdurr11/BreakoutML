import os, sys
# sys.path.append(os.path.abspath('.'))
from bodies import Block, Paddle, Ball
from vector import Vector
import random
import math
# from .bodies import Block

BALL_VELOCITY_MAGINITUDE = 8
class Game():
    def __init__(self, rows, columns, block_size, height = 10):
        self.rows = rows
        self.columns = columns
        self.block_size = block_size
        self.height = height
        self.pixel_height = height * block_size
        #game_state = 'PLAYING', 'LOST', 'PAUSED', 'WON'
        self.game_state = 'PLAYING'
        #in pixels
        self.pixel_width = ( columns + 2 ) * block_size
        self.blocks = self.initialize_blocks()
        self.paddle = Paddle((self.pixel_width//2 - block_size//2, self.pixel_height - block_size), block_size, 10)
        self.ball = Ball((self.pixel_width//2 - block_size//2, self.pixel_height//2), 6, self.make_initial_velocity())
        self.score = 0
        self.intersected_paddle = False
        self.intersected_block = False
        self.initialize_blocks()

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
            self.paddle.update_position(Vector(-(self.block_size//5),0))
            paddle_pos_x = self.paddle.get_position()[0]
            #inside the left wall
            if paddle_pos_x < self.block_size:
                translation_vector = Vector(self.block_size - paddle_pos_x, 0)
                self.paddle.update_position(translation_vector)

        elif (keys['right']):
            self.paddle.update_position(Vector(self.block_size//5,0))
            paddle_pos_x = self.paddle.get_position()[0]
            #inside right wall
            if paddle_pos_x + self.paddle.get_width() > self.get_pixel_width() - self.block_size:
                right_overlap = (paddle_pos_x + self.paddle.get_width()) - (self.get_pixel_width() - self.block_size)
                translation_vector = Vector(-right_overlap, 0)
                self.paddle.update_position(translation_vector)

    #keys {'left' : Boolean, 'right' : Boolean}
    def time_step(self, keys):
        self.intersected_paddle = False
        self.intersected_block = False

        if (self.score == self.rows * self.columns):
            self.game_state = 'WON'

        if self.game_state == 'PLAYING':
            self.update_paddle(keys)
            self.ball.update_position_auto()
            for block in self.blocks:
                if block.get_exists():
                    if self.ball.intersects_block(block):
                        self.ball.resolve_collision_block(block)
                        if block.is_soft():
                            self.score += 1
                            block.remove_block()
                        self.intersected_block = True

            if self.ball.intersects_paddle(self.paddle):
                self.intersected_paddle = True
                self.ball.resolve_collision_paddle(self.paddle)

            if (not self.check_ball_in_bounds(self.ball)):
                self.game_state = 'LOST'



        #first update paddle
        #cancel each other out


    #returns true if the ball is in bounds, false otherwise
    def check_ball_in_bounds(self, ball):
        if ball.get_center()[1] > self.pixel_height:
            return False
        return True


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

    def get_game_state(self):
        return self.game_state

    def get_paddle_location_json(self):
        return {'x' : self.paddle.get_position()[0],
                'y' : self.paddle.get_position()[1],
                'width' : self.paddle.get_width()}

    def get_ball_location_json(self):
        return {'x' : self.ball.get_center()[0],
                'y' : self.ball.get_center()[1],
                }

    def get_score(self):
        return self.score

    def did_intersect_paddle(self):
        return self.intersected_paddle

    def did_intersect_block(self):
        return self.intersected_block

    def make_initial_velocity(self):
        #Get a random angle value between 10 and 30
        angle = random.randint(30,60)
        rad_angle = math.radians(angle)
        horizontal_velocity = math.sin(rad_angle) * BALL_VELOCITY_MAGINITUDE
        vertical_velocity = math.cos(rad_angle) * BALL_VELOCITY_MAGINITUDE
        random_negate = 1 if random.random() < 0.5 else -1
        return Vector(random_negate*horizontal_velocity, vertical_velocity)



    def get_blocks_json(self):
        final_blocks_json = []
        for block in self.blocks:
            if block.get_exists():
                final_blocks_json.append(
                    {
                        'x': block.get_position()[0],
                        'y': block.get_position()[1],
                        'type' : block.get_type(),
                        'exists' : block.get_exists(),
                        'color' : block.get_color(),
                    })

        return final_blocks_json;

    def get_game_state_vector(self):
        ball_center_x = self.ball.get_center()[0]
        ball_center_y = self.ball.get_center()[1]
        ball_vel_x = self.ball.get_velocity().get_x()
        ball_vel_y = self.ball.get_velocity().get_y()
        paddle_pos_x = self.paddle.get_position()[0]
        paddle_pos_y = self.paddle.get_position()[1]

        return (ball_center_x, ball_center_y, \
                ball_vel_x, ball_vel_y, \
                paddle_pos_x, paddle_pos_y)
