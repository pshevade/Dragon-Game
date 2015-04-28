#
# character_class - everything that appears on the map is a character:
#                   the player's dragon is derived from character class,
#                   the enemies are derived from character class, and
#                   the buildings in the city are also derived from character class
#

from game_constants import *

class Character(pygame.sprite.Sprite):

    def __init__(self, start_tile):
        pygame.sprite.Sprite.__init__(self)
        self.current_tile = start_tile


    def get_xy_co-ordinates(self):
        row = (self.tile_no - 1) / TILES
        col = (self.tile_no) % TILES
        if col == 0 :
            col = TILES
        return (row, col)

def main():



