from vector import Vector
class BLOCK_TYPES:
    BORDER = 0
    NORMAL = 1


class Body():
    def __init__( self, position):
        self.position = position

    #Updates the position of the body
    #@param velocity_vector : A vector with an x and y component
    def update_position(velocity_vector):
        pass

    def get_position(self):
        return self.position

class Block(Body):
    def __init__( self, position, type, side_length, exists = True):
        self.type = type
        self.exists = exists
        self.side_length = side_length
        super().__init__(position)

    def update_position(velocity_vector):
        raise Exception("Tried to update position of Block")

    def get_type(self):
        return self.type

    def get_exists(self):
        return self.exists

    def get_position(self):
        return self.position

    def get_side_length(self):
        return self.side_length


class Paddle(Body):
    def __init__( self, position, width, height):
        super().__init__(position)
        self.position = position
        self.width = width
        self.paddle_height = height

    def update_position(self, velocity_vector):
        assert velocity_vector.get_y() == 0
        self.position = (self.position[0] + velocity_vector.get_x(),
                        self.position[1] + velocity_vector.get_y())

    def get_width(self):
        return self.width

    def get_height(self):
        return self.paddle_height

class Ball(Body):
    def __init__(self, center, radius, velocity = Vector(6,-6)):
        self.center = center
        self.radius = radius
        self.velocity = velocity

    def update_position_auto(self):
        self.center = (self.center[0] + self.velocity.get_x(),
                        self.center[1] + self.velocity.get_y())

    def update_position_manual(self, translation_vector):
        self.center = (self.center[0] + translation_vector.get_x(),
                        self.center[1] + translation_vector.get_y())

    def get_center(self):
        return self.center

    def get_velocity(self):
        return self.velocity
    #Determines if there is an intersection between the ball and another body
    #@param : other_body another body that exists in the game
    #@return : true if the other body intersects the ball, false otherwise
    def intersects_block(self, other_block):
        ball_left_x = self.center[0] - self.radius
        ball_right_x = self.center[0] + self.radius
        ball_top_y = self.center[1] - self.radius
        ball_bottom_y = self.center[1] + self.radius

        if ball_left_x > other_block.get_position()[0] + other_block.get_side_length():
            return False

        if ball_right_x < other_block.get_position()[0]:
            return False

        if ball_bottom_y < other_block.get_position()[1]:
            return False

        if ball_top_y > other_block.get_position()[1] + other_block.get_side_length():
            return False

        return True

    #returns the min_dist and updates the ball position and direction
    def resolve_collision_block(self, other_body):
        left_ball_bound = self.center[0] - self.radius, self.center[1]
        right_ball_bound = self.center[0] + self.radius, self.center[1]
        bottom_ball_bound = self.center[0], self.center[1] + self.radius
        top_ball_bound = self.center[0], self.center[1] - self.radius

        block_left = other_body.get_position()[0]
        block_right = other_body.get_position()[0] + other_body.get_side_length()
        block_top = other_body.get_position()[1]
        block_bottom = other_body.get_position()[1] + other_body.get_side_length()

        # distance_from_top = (bottom_ball_bound - self.center[1])
        # distance_from_bottom = (other_body.get_position()[1] + other_body.get_side_length()) - self.center[1]
        # distance_from_left = self.center[0] - other_body.get_position()[0]
        # distance_from_right =  (other_body.get_position()[0] + other_body.get_side_length()) - self.center[0]

        # min_dist = min(distance_from_top, distance_from_left, distance_from_bottom, distance_from_right)
        #hitting the left side of the block
        if (right_ball_bound[0] >= block_left \
        and right_ball_bound[0] <= block_right \
        and right_ball_bound[1] >= block_top \
        and right_ball_bound[1] <= block_bottom):
            distance_from_left = right_ball_bound[0] - block_left
            self.update_position_manual(Vector(-distance_from_left - 1, 0))
            self.velocity = self.velocity.reflect_x()
            print("1")
            # assert False

        #hitting the right side of the block
        if (left_ball_bound[0] <= block_right \
        and left_ball_bound[0] >= block_left \
        and left_ball_bound[1] >= block_top \
        and left_ball_bound[1] <= block_bottom):
            distance_from_right = block_right - left_ball_bound[0]
            self.update_position_manual(Vector(distance_from_right + 1, 0))
            self.velocity = self.velocity.reflect_x()
            print("2")

        #hitting the  bottom of the block
        if (top_ball_bound[1] <= block_bottom \
        and top_ball_bound[1] >= block_top \
        and top_ball_bound[0] <= block_right \
        and top_ball_bound[0] >= block_left):
            distance_from_bottom = block_bottom - top_ball_bound[1]
            self.update_position_manual(Vector(0, distance_from_bottom + 1))
            self.velocity = self.velocity.reflect_y()


        #hitting the top of the block
        if (bottom_ball_bound[1] >= block_top \
        and bottom_ball_bound[1] <= block_bottom \
        and bottom_ball_bound[0] <= block_right \
        and bottom_ball_bound[0] >= block_left):
            distance_from_top = bottom_ball_bound[1] - block_top
            self.update_position_manual(Vector(0, -distance_from_top - 1))
            self.velocity = self.velocity.reflect_y()


    def intersects_paddle(self, paddle):
        bottom_ball_bound = self.center[0], self.center[1] + self.radius

        paddle_left = paddle.get_position()[0]
        paddle_right = paddle.get_position()[0] + paddle.get_width()
        paddle_top = paddle.get_position()[1]
        paddle_bottom = paddle.get_position()[1] + paddle.get_height()


        if (bottom_ball_bound[1] >= paddle_top \
        and bottom_ball_bound[1] <= paddle_bottom \
        and bottom_ball_bound[0] <= paddle_right \
        and bottom_ball_bound[0] >= paddle_left):
            return True


    def resolve_collision_paddle(self, paddle):
        bottom_ball_bound = self.center[0], self.center[1] + self.radius
        distance_from_top = bottom_ball_bound[1] - paddle.get_position()[1]
        self.update_position_manual(Vector(-distance_from_top - 1, 0))
        self.velocity = self.velocity.reflect_y()
