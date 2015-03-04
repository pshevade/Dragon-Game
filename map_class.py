#
# map class
#

import pygame
import sys
from pygame.locals import *
from game_constants import *
from tile_class import *

class LevelMap():
    ''' LevelMap class : contains all information to set up the level map
                         The map is made up of Tile class objects - tiles
                         The map is scrollable and calculates offsets based on mouse movement
                         The mouse clicks are converted into tile numbers here

        attributes:
        methods:
    '''

    def __init__(self):
        self.offsetx = 0    #offset along the x axis when map is dragged with mouse
        self.offsety = 0    #offset along the y axis
        self.tile_list = []
        self.tile_dict = {}
        self.display = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))


    def initialize_tiles(self):
        ''' Initialize the bare bones tiles of the map '''
        count = 1
        for y in range(1, TILES+1):
            tiley = WINDOWSIZE - y*TILESIZE
            for x in range(0, TILES):
                tilex = x*TILESIZE
                self.tile_list.append(Tile("empty", count,
                                           tilex, tiley,
                                           TILESIZE, TILESIZE))
                count +=1

    def draw_tiles(self):
        ''' Draw the tiles that are within the window to the screen
            If we have 1000 tiles, and can see only 100 in the display screen,
            we don't want to draw the 900 others. We only want to see the 100 visible
            tiles. This function figures out which of the tiles are currently visible
            and only draws those '''

        for tile in self.tile_list:
            tile.x += self.offsetx
            tile.y += self.offsety
            if tile.x >= -TILESIZE and tile.x < WINDOWSIZE+TILESIZE and tile.y >= -TILESIZE and tile.y < WINDOWSIZE+TILESIZE:
                pygame.draw.rect(self.display, tile.color, tile, 1)
                self.text_to_screen(tile.number, tile.x+TILESIZE/2, tile.y+TILESIZE/2)



    def from_xy_to_tile_no(self, point):
        point_on_tile_no = 0
        for tile in self.tile_list:
            if tile.collidepoint(point):
                point_on_tile_no = tile.number

        return point_on_tile_no

    #def get_draw_list(self):


    def set_drag_offsets(self, offsets):
        self.offsetx = offsets[0]
        self.offsety = offsets[1]
        #print(offsets)


    def text_to_screen(self, text, x, y, size = 10,
                    color = (255, 255, 255), font_type = 'monospace'):

        text = str(text)
        font = pygame.font.SysFont('monospace', size)
        text = font.render(text, True, color)
        self.display.blit(text, (x,y))



def main():
    my_map = LevelMap()
    my_map.initialize_tiles()
    pygame.init()
    drag_flag = 0
    button3 = 0
    while True:
        my_map.display.fill(BLACK)
        (button1, button2, button3) = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # mousebutton down event generated, and the right-click is pressed
            # then we can begin the map dragging
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                drag_flag = 1
                #print(my_map.from_xy_to_tile_no(pygame.mouse.get_pos()))
                # since we want the relative mouse position from the point of
                # right click, and not between some previous point and point of
                # right click, we flush the first result of get_rel():
                pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[2]:
                drag_flag = 0
                # we want to set the drag offsets to zero when the right click
                # is depressed
                my_map.set_drag_offsets((0,0))

        if drag_flag:
            my_map.set_drag_offsets(pygame.mouse.get_rel())




        my_map.draw_tiles()

        pygame.display.flip()

if __name__ == '__main__':
    main()
