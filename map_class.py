#
# map class
#

import pygame
import sys
from pygame.locals import *
from game_constants import *
from tile_class import *
import random
import a_star_class
import unittest


class LevelMap(pygame.sprite.Group):
    ''' LevelMap class : contains all information to set up the level map
                         The map is made up of Tile class objects - tiles
                         The map is scrollable and calculates offsets based on mouse movement
                         The mouse clicks are converted into tile numbers here
        : inherits:      pygame's sprite Group class, to hold the characters
                         some important pygame.sprite.Group methods -
                            .sprites() - list of all sprites in this Group
                            .add(*sprites) - add any num. of sprites to this Group
                            .remove(*sprites) - remove any num. of sprites from this group
                            .draw(surface) - draws the contained sprites to surface
        : attributes:
        : methods:
    '''

    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.offsetx = 0    #offset along the x axis when map is dragged with mouse
        self.offsety = 0    #offset along the y axis
        self.tile_list = []
        self.display = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
        self.road = []


    def map_creator(self):
        """ This function will generate a random map, with a road that the sprites can
            move on and buildings """
        self.initialize_tiles()         # first create an empty tile grid
        self.draw_road_thru_map()       # generate a random road (self.road)
        self.draw_buildings()           # fill the remaining tiles with buildings


    def initialize_tiles(self):
        ''' Initialize the bare bones tiles of the map '''
        count = 1
        for y in range(TILESIZE, (TILES+1)*TILESIZE, TILESIZE):
            tiley = WINDOWSIZE - y
            for x in range(0, TILES*TILESIZE, TILESIZE):
                tilex = x
                self.tile_list.append(Tile("empty", count,
                                           tilex, tiley,
                                           TILESIZE, TILESIZE))
                count +=1


    def draw_buildings(self):
        """ Set tiles which are not part of the road to buildings """
        for tile in self.tile_list:
            if tile.number not in self.road:
                tile.type = 'city'
                tile.set_images()
                tile.set_walkability()


    def draw_road_thru_map(self):
        """ This method will create roads.
            Roads are created by using the A-Star algorithm. We get a "path" from
            a start tile to the "next" tile (generated randomly). The tiles along
            this path are converted to 'road' type.
        """
        # road_dist_x is a list of distances to the next tile along x-axis
        road_dist_x = [x for x in range(0, TILES//2)]
        # road_dist_y is a list of distances to the next tile along y-axis
        road_dist_y = [x for x in range(0, TILES*TILES//2, TILES)]

        # the distances are used to get the next tile = start + dist_x + dist_y
        #                                  ex. next_tile = 1 + 3 + 30 = 34
        #                                  so tile 34 will be the target for AStar
        # we only look at half the possible distances (TILES//2 or TILES*TILES//2)
        # because we don't want to get the tiles further than the max, TILES*TILES

        random.shuffle(road_dist_x)     # so we get a different tile each time
        random.shuffle(road_dist_y)     # so we get a different tile each time
        start_tile = 1                  # start on tile no. 1 (FUTURE UPDATE - change the start location)
        road_plan = a_star_class.A_Star()

        # We will call the draw_road_segment() function to get pieces of the road
        # until we go from tile 1 (very beginning tile) to tile max (the tile to reach to win)
        while len(road_dist_x) > 0:
            next_tile = start_tile + road_dist_x.pop() + road_dist_y.pop()
            # If the starting tile is in the top row, the next tile should be last tile
            if start_tile > TILES*(TILES-1):
                next_tile = TILES*TILES
            # If the next tile is to the left of the start tile, go up a row (so road doesn't wrap on itself)
            if next_tile%TILES < start_tile%TILES:
                next_tile+=TILES
            # if the next tile is higher than the max possible tile, reset it to the max tile
            if next_tile > TILES*TILES:
                next_tile = TILES*TILES

            self.draw_road_segment(start_tile, next_tile, road_plan)
            start_tile = next_tile

        # Remove the repeated tiles
        for point in self.road:
            indx = self.road.index(point)
            if point in self.road[indx+1:]:
                self.road.remove(point)
        # We want road segments to connect to the main road from the 2 other corners too
        # First we connect the bottom right corner to a lower part of the road (look at the first half of the list)
        self.draw_road_segment(TILES, random.choice(self.road[:len(self.road)//2]), road_plan)
        # Then we connect the top left corner to a higher part of the road (second half of the list)
        self.draw_road_segment(TILES*(TILES-1) + 1, random.choice(self.road[len(self.road)//2:]), road_plan)
        # Change the tiles in the map to road
        for tile in self.tile_list:
            if tile.number in self.road:
                tile.type = 'road'
                tile.set_colors()
                tile.set_walkability()


    def draw_road_segment (self, start_tile, next_tile, road_plan):
        """ This method will give us the path from the start tile to the next tile -
            giving us the segment of the road, which we will append to self.road
        """
        road_plan.init_AStar(self.return_dict_of_tiles(), start_tile, next_tile)
        road_plan.run_AStar(start_tile)
        segment = road_plan.get_path()
        segment.reverse()
        self.road += segment
        road_plan.reset()
        start_tile = next_tile


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
                if tile.type == 'road' or tile.type == 'empty':
                    pygame.draw.rect(self.display, tile.color, tile)
                    self.text_to_screen(tile.number, tile.x+TILESIZE/2, tile.y+TILESIZE/2)
                elif tile.type == 'city':
                    img = pygame.image.load(tile.img_path)
                    self.display.blit(img, (tile.x, tile.y))


    def from_xy_to_tile_no(self, point):
        """ Return the tile number of the tile that contains the mouse click x,y in """
        point_on_tile_no = 0
        for tile in self.tile_list:
            if tile.collidepoint(point):
                point_on_tile_no = tile.number

        return point_on_tile_no


    def set_drag_offsets(self, offsets):
        """ Scrolled offsets are stored and used to calculate how to render the map """
        self.offsetx = offsets[0]
        self.offsety = offsets[1]


    def text_to_screen(self, text, x, y, size = 10,
                    color = (255, 255, 255), font_type = 'monospace'):

        text = str(text)
        font = pygame.font.SysFont('monospace', size)
        text = font.render(text, True, color)
        self.display.blit(text, (x,y))


    def return_dict_of_tiles(self):
        return {tile.number: tile for tile in self.tile_list}


class TestLevelMap(unittest.TestCase):
    def setUp(self):
        self.test_map = LevelMap()
        self.test_map.initialize_tiles()
        self.test_map.draw_road_thru_map()

    def test_total_tiles(self):
        self.assertEqual(len(self.test_map.tile_list), TILES*TILES,
                        "Incorrect number of tiles created: Expected {0}, saw {1}".format(TILES*TILES, len(self.test_map.tile_list)))

    def test_return_dict_of_tiles(self):
        test_dict = self.test_map.return_dict_of_tiles()
        for tile_no in range(1, TILES*TILES):
            self.assertEqual(test_dict[tile_no].number, self.test_map.tile_list[tile_no-1].number, "Tiles dictionary to tiles list mismatch: at tile {0}".format(tile_no))



def main():
    my_map = LevelMap()
    my_map.map_creator()
    #my_map.initialize_tiles()
    #my_map.draw_road_thru_map()
    pygame.init()
    drag_flag = 0
    button3 = 0
    while True:
        my_map.display.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # mousebutton down event generated, and the right-click is pressed
            # then we can begin the map dragging
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                drag_flag = 1
                # since we want the relative mouse position from the point of
                # right click, and not between some previous point and point of
                # right click, we flush the first result of get_rel():
                pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[2]:
                drag_flag = 0
                # we want to set the drag offsets to zero when the right click
                # is depressed
                my_map.set_drag_offsets((0,0))

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                print("Clicked on tile: {0}".format(my_map.from_xy_to_tile_no(pygame.mouse.get_pos())))


        if drag_flag:
            my_map.set_drag_offsets(pygame.mouse.get_rel())

        my_map.draw_tiles()

        pygame.display.flip()


if __name__ == '__main__':
    #unittest.main()
    main()
