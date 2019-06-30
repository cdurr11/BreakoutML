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


class Paddle(Body):
    def __init__( self, position, width):
        super().__init__(position)
        self.position = position
        self.width = width

    def update_position(self, velocity_vector):
        assert velocity_vector.get_y() == 0
        print(self.position)
        self.position = (self.position[0] + velocity_vector.get_x(),
                        self.position[1] + velocity_vector.get_y())

    def get_width(self):
        return self.width

class Ball(Body):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def update_position(velocity_vector):
        pass

    #Determines if there is an intersection between the ball and another body
    #@param : other_body another body that exists in the game
    #@return : true if the other body intersects the ball, false otherwise
    def intersects(other_body):
        pass
