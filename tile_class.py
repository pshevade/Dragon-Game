#
# tile_class - contains the Tile class for this tile based game
#

import pygame
from pygame.locals import *
from game_constants import *

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
        self.color = GREEN
        self.setColors()

    def setColors(self):
        ''' Sets the color of the tile depending on what its type is
            Used for testing before the actual image is introduced '''
        if self.type is 'empty':
            self.color = GREEN
        elif self.type is 'city':
            self.color = BLUE
        elif self.type is 'road':
            self.color = GRAY

    def getTileInfo(self):
        ''' Returns the tile information as a tuple '''
        return (self.number, self.type)


def main():
    tile1 = Tile('empty', 1, 0, 0, TILESIZE, TILESIZE)
    tile2 = Tile('city', 1, 80, 0, TILESIZE, TILESIZE)
    tile3 = Tile('road', 1, 0, 80, TILESIZE, TILESIZE)
    tile4 = Tile('empty', 1, 80, 80, TILESIZE, TILESIZE)

    print("Tile 1 has color: {0} and it's details are {1}".format(tile1.color, tile1.getTileInfo()))
    print("Tile 2 has color: {0} and it's details are {1}".format(tile2.color, tile2.getTileInfo()))
    print("Tile 3 has color: {0} and it's details are {1}".format(tile3.color, tile3.getTileInfo()))
    print("Tile 4 has color: {0} and it's details are {1}".format(tile4.color, tile4.getTileInfo()))


if __name__ == '__main__':
    main()
