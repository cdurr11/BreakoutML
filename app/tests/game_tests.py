import unittest, os, sys
sys.path.append(os.path.abspath('..'))
from src.game import Game

class TestGame(unittest.TestCase):
    #test get blocks/ initialize_block
    def test_initialize_blocks_multiple(self):

        game = Game(2,3,30)
        game.initialize_blocks()
        blocks = game.get_blocks()

        for block in blocks:
            print("position: ", block.get_position(), "type: ", block.get_type())
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


    #tests works with one block
    # def test_initialize_single_block(self):
    #     game = Game(1,1,30)
    #     game.initialize_blocks()
    #     blocks = game.get_blocks()
    #     self.assertEqual(blocks[0][0].get_position()[0], 30)
    #     self.assertEqual(blocks[0][0].get_position()[1], 60)











if __name__ == '__main__':
    unittest.main()
