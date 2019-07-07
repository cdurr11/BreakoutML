import unittest, os, sys
sys.path.append(os.path.abspath('..'))
from game import Game
from bodies import Ball, Block
from vector import Vector
# from src.game import Game
# from src.bodies import Ball, Block

class TestGame(unittest.TestCase):
    #test get blocks/ initialize_block
    def test_initialize_blocks_multiple(self):

        game = Game(2,3,30)
        game.initialize_blocks()
        blocks = game.get_blocks()

        # for block in blocks:
            # print("position: ", block.get_position(), "type: ", block.get_type())
        #
        self.assertEqual(len(blocks), 29)

        #check 0 row
        for i in range(5):
            self.assertEqual(blocks[i].get_position()[0], 30*i)
            self.assertEqual(blocks[i].get_position()[1], 0)
            self.assertEqual(blocks[i].get_type(), "HARD")

        #check 1 row
        for j in range(5):
            self.assertEqual(blocks[j + 5].get_position()[0], 30*j)
            self.assertEqual(blocks[j + 5].get_position()[1], 30)
            if j == 0 or j == 4:
                self.assertEqual(blocks[j + 5].get_type(), "HARD")
            else:
                self.assertEqual(blocks[j + 5].get_type(), "SOFT")

        #check 2 row
        for k in range(5):
            self.assertEqual(blocks[k + 10].get_position()[0], 30*k)
            self.assertEqual(blocks[k + 10].get_position()[1], 60)
            if k == 0 or k == 4:
                self.assertEqual(blocks[k + 10].get_type(), "HARD")
            else:
                self.assertEqual(blocks[k + 10].get_type(), "SOFT")

        #check left wall
        for l in range(7):
            self.assertEqual(blocks[15 + 2*l].get_position()[0], 0)
            self.assertEqual(blocks[15 + 2*l].get_position()[1], l*30 + 90)
            self.assertEqual(blocks[15 + 2*l].get_type(), "HARD")

        #check right wall
        for m in range(7):
            self.assertEqual(blocks[16 + 2*m].get_position()[0], 120)
            self.assertEqual(blocks[16 + 2*m].get_position()[1], m*30 + 90)
            self.assertEqual(blocks[16 + 2*m].get_type(), "HARD")

class TestBall(unittest.TestCase):
    def test_does_intersect(self):
        #test intersects left
        ball0 = Ball((0,2), 3)
        block0 = Block((1,0), "HARD",  5)
        self.assertTrue(ball0.intersects_block(block0))

        #test intersects top
        ball1 = Ball((2,0), 3)
        block1 = Block((0,3), "HARD",  5)
        self.assertTrue(ball1.intersects_block(block1))

        #test intersects bottom
        ball2 = Ball((2,8), 3)
        block2 = Block((0,2), "HARD",  5)
        self.assertTrue(ball2.intersects_block(block2))

        #test intersects right
        ball3 = Ball((6,3), 3)
        block3 = Block((0,2), "HARD",  5)
        self.assertTrue(ball3.intersects_block(block3))

    def test_does_not_intersect(self):

        #test does not intersect left
        ball0 = Ball((0,2), 1)
        block0 = Block((2,0), "HARD",  5)
        self.assertFalse(ball0.intersects_block(block0))

        #test does not intersect top
        ball1 = Ball((2,0), 3)
        block1 = Block((0,4), "HARD",  5)
        self.assertFalse(ball1.intersects_block(block1))

        #test does not intersect bottom
        ball2 = Ball((2,9), 3)
        block2 = Block((0,0), "HARD",  5)
        self.assertFalse(ball2.intersects_block(block2))

        #test does not intersect right
        ball3 = Ball((9,3), 3)
        block3 = Block((0,2), "HARD",  5)
        self.assertFalse(ball3.intersects_block(block3))

    #tests resolution when ball intersects the left of the square
    def test_resolve_on_left(self):
        ball = Ball((0,2), 3, Vector(1,1))
        block = Block((1,0), "HARD",  5)
        ball.resolve_collision_block(block)
        self.assertEqual(ball.get_velocity(), Vector(-1,1))
        self.assertEqual(ball.get_center(), (-3, 2))

    #tests resolution when ball intersects the top of the square
    def test_resolve_on_top(self):
        ball = Ball((2,0), 3, Vector(1,1))
        block = Block((0,3), "HARD",  5)
        ball.resolve_collision_block(block)
        self.assertEqual(ball.get_velocity(), Vector(1,-1))
        self.assertEqual(ball.get_center(), (2, -1))

    #tests resolution when ball intersects the bottom of the square
    def test_resolve_on_bottom(self):
        ball = Ball((2,8), 3, Vector(1,1))
        block = Block((0,2), "HARD",  5)
        ball.resolve_collision_block(block)
        self.assertEqual(ball.get_velocity(), Vector(1,-1))
        self.assertEqual(ball.get_center(), (2, 11))

    #tests resolution when ball intersects the right of the square
    def test_resolve_on_right(self):
        ball = Ball((6,3), 3, Vector(1,1))
        block = Block((0,2), "HARD",  5)
        ball.resolve_collision_block(block)
        self.assertEqual(ball.get_velocity(), Vector(-1, 1))
        self.assertEqual(ball.get_center(), (9, 3))

    def check_game_ends_when_ball_is_out(self):
        game = Game(2,3,30)
        ball = Ball((40,91))
        self.assertFalse(game.check_ball_in_bounds(ball))

        ball = Ball((40,89))
        self.assertTrue(game.check_ball_in_bounds(ball))

if __name__ == '__main__':
    unittest.main()
