#
# tile_class - contains the Tile class for this tile based game
#

import pygame
from pygame.locals import *
from game_constants import *
import random
import unittest

IMAGE_LIST = ['building1.png', 'building2.png', 'building3.png', 'building4.png']


class Tile(pygame.Rect):
    ''' Tile class : contains information regarding the tiles
                     that are the building blocks of the map

                     class derrives from the pygame Rect class

        attributes: x,y - rectangle upper left corner coordinates
                    height, width - of the rectangle
                    number - each tile gets a number - for AStar search
                    tile_type - determines walkability/image of tile_type

        methods:    setColors - for testing purposes, tile color is determined
                    by the tile_type. This method will be useless when we introduce
                    actual images for the tiles

                    getTileInfo - returns the tile number and tile type as a tuple

    '''
    def __init__(self, tile_type, tile_num, x, y, height, width):
        pygame.Rect.__init__(self, x, y, height, width)
        self.number = tile_num
        self.type = tile_type
        self.color = WHITE
        self.img_path = ""

        self.walkability = 0        # The walkability depends on the type of tile
        self.gval = 0
        self.hval = 0
        self.fval = 0
        self.parent = 0

        self.set_colors()
        self.set_images()
        self.set_walkability()


    def set_walkability(self):
        if self.type is 'empty':
            self.walkability = 20
        elif self.type is 'city':
            self.walkability = 100
        elif self.type is 'road':
            self.walkability = 1


    def set_images(self):
        ''' Sets the color of the tile depending on what its type is
            Used for testing before the actual image is introduced '''
        if self.type is 'empty':
            self.img_path = ""
        elif self.type is 'city':
            self.img_path = 'artwork/' + random.choice(IMAGE_LIST)
        elif self.type is 'road':
            self.img_path = ""


    def set_colors(self):
        ''' Sets the color of the tile depending on what its type is
            Used for testing before the actual image is introduced '''
        if self.type is 'empty':
            self.color = WHITE
        elif self.type is 'city':
            self.color = BLUE
        elif self.type is 'road':
            self.color = GRAY

    def get_tile_info(self):
        ''' Returns the tile information as a tuple '''
        return (self.number, self.type)


    def reset_for_AStar(self):
        self.gval = 0
        self.fval = 0
        self.hval = 0
        self.parent = 0



class TileTest(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile('empty', 1, 0, 0, TILESIZE, TILESIZE)
        self.tile2 = Tile('city', 2, 80, 0, TILESIZE, TILESIZE)
        self.tile3 = Tile('road', 3, 0, 80, TILESIZE, TILESIZE)
        self.tile4 = Tile('empty', 4, 80, 80, TILESIZE, TILESIZE)

    def test_walkability(self):
        self.assertEqual(self.tile1.walkability, 20, "Wrong walkability set!")
        self.assertEqual(self.tile2.walkability, 100, "Wrong walkability set!")
        self.assertEqual(self.tile3.walkability, 1, "Wrong walkability set!")
        self.assertEqual(self.tile4.walkability, 20, "Wrong walkability set!")

    def test_info(self):
        self.assertEqual(self.tile1.get_tile_info(), (1, 'empty'), "Wrong tile information set!")
        self.assertEqual(self.tile2.get_tile_info(), (2, 'city'), "Wrong tile information set!")
        self.assertEqual(self.tile3.get_tile_info(), (3, 'road'), "Wrong tile information set!")
        self.assertEqual(self.tile4.get_tile_info(), (4, 'empty'), "Wrong tile information set!")


if __name__ == '__main__':
    unittest.main()
    main()
