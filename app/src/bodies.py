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

class Block(Body):
    def __init__( self, position, type, side_length, exists = True):
        self.type = type
        self.exists = exists
        self.side_length = side_length
        super().__init__(position)

    def update_position(velocity_vector):
        raise Exception("Tried to update position of Block")

class Paddle(Body):
    def __init__( self, position):
        super().__init__(position)

    def update_position(velocity_vector):
        pass

class Ball(Body):
    def __init__(self, position, radius):
        super().__init__(position)

    def update_position(velocity_vector):
        pass

    #Determines if there is an intersection between the ball and another body
    #@param : other_body another body that exists in the game
    #@return : true if the other body intersects the ball, false otherwise
    def intersects(other_body):
        pass
