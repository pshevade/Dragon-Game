# A Star algorithm

import pygame
from pygame.locals import *
from game_constants import *
import unittest
import map_class

class A_Star():

    def __init__(self):
        self.tile_dict = {}
        self.start = 0
        self.target = 0
        self.closed_list = []
        self.open_list = []
        self.path_list = []
        self.LFT = 0


    def get_surrounding_tiles(self, tile):
        #print("\n")
        #print("xxxx get_surrounding_tiles xxxx")
        #print("The center tile: {0}".format(tile))
        surrounding_list = [tile+N, tile+E, tile+S, tile+W]
        #print("These are the surrounding tiles, raw: {0}".format(surrounding_list))
        # we want to remove tile number that are either OFF the grid
        # ex. tile 1 will get tile 0 to its west.

        rem_list = [] # list of tiles to remove from surrounding_list
        if tile % TILES == 0 and tile+E not in rem_list:
            rem_list.append(tile+E)
            #print("Removing east tile: {0}".format(tile+E))
        if tile % TILES == 1 and tile+W not in rem_list:
            rem_list.append(tile+W)
            #print("Removing west tile: {0}".format(tile+W))
        if (tile-1) / TILES <= 1 and tile+S not in rem_list:
            rem_list.append(tile+S)
            #print("Removing south tile: {0}".format(tile+S))
        if (tile-1) / TILES >= TILES-1 and tile+N not in rem_list:
            rem_list.append(tile+N)
            #print("Removing north tile: {0}".format(tile+N))
        # We also want to remove all tiles that have already been added to
        # closed list (so we don't traverse them again)
        for x in self.closed_list:
            if x not in rem_list:
                rem_list.append(x)
        #print("These are tiles to be removed: {0}".format(rem_list))
        # Finally, remove the unwanted tiles from the surrounding_tiles list
        for tile in rem_list:
            if tile in surrounding_list:
                surrounding_list.remove(tile)
        #print("Finally, the surrounding tiles are: {0}".format(surrounding_list))


        return surrounding_list


    def set_all_hvals(self):
        targetx = (self.target-1)%TILES
        targety = (self.target-1)/TILES + 1

        for tile in self.tile_dict:
            tilex = (tile-1)%TILES
            tiley = (tile-1)/TILES + 1
            self.tile_dict[tile].hval = 10*(abs(targetx-tilex)+abs(targety-tiley))


    def set_gval(self, cur_gval, dest_tile):
        self.tile_dict[dest_tile].gval += cur_gval*self.tile_dict[dest_tile].walkability


    def set_fval(self, dest_tile):
        self.tile_dict[dest_tile].fval = self.tile_dict[dest_tile].gval + self.tile_dict[dest_tile].hval



    def init_AStar(self, tile_dict, start, target):
        if len(self.tile_dict) < 1:
            self.tile_dict = tile_dict
        self.start = start
        self.target = target

        self.open_list.append(start)
        self.set_all_hvals()


    def find_LFT(self):
        possibleFVals = []
        for tile_no in self.open_list:
            possibleFVals.append(self.tile_dict[tile_no].fval)

        for tile_no in self.open_list:
            if self.tile_dict[tile_no].fval == min(possibleFVals):
                return tile_no

        return tile_no


    def get_cost(self, source_tile_no, dest_tile_no):
        diff = source_tile_no - dest_tile_no
        if diff in (N,S,E,W):
            return 10
        if diff in (NW, NE, SW, SE):
            return 14


    def run_AStar(self, current_tile_no):
        #print("\nxxxx run_AStar xxxx")
        #print("Current tile is: {0}".format(current_tile_no))
        if current_tile_no == self.target:
            #print("Returning tile: {0}, which is same as target: {1}".format(current_tile_no, self.target))
            return current_tile_no
        else:
            self.open_list.remove(current_tile_no)
            self.closed_list.append(current_tile_no)
            #print("Removed tile from open_list, which looks like: {0}".format(self.open_list))
            surrounding_tiles = self.get_surrounding_tiles(current_tile_no)
            #print("Removed tile from open_list, which looks like: {0}".format(surrounding_tiles))
            for tile_no in surrounding_tiles:
                if tile_no not in self.open_list:
                    self.tile_dict[tile_no].parent = current_tile_no
                    self.set_gval(   self.tile_dict[current_tile_no].gval +
                                    self.get_cost(current_tile_no, tile_no),
                                    tile_no)
                    self.set_fval(tile_no)
                    self.open_list.append(tile_no)

                elif tile_no in self.open_list:
                    if (self.get_cost(current_tile_no, tile_no) + self.tile_dict[current_tile_no].gval) * self.tile_dict[tile_no].walkability < self.tile_dict[tile_no].gval:
                        self.tile_dict[tile_no].parent = current_tile_no

            self.LFT = self.find_LFT()
            #print("Next tile to go to is: {0}".format(self.LFT))
            self.run_AStar(self.LFT)
            return self.LFT


    def get_path(self):
        #print("\nxxxx get_path xxxx")
        tile_no = self.target
        #print("Starting at: {0}".format(tile_no))
        while tile_no is not self.start:
            self.path_list.append(tile_no)
            #print("Next node is: {0}".format(tile_no))
            tile_no = self.tile_dict[tile_no].parent
        self.path_list.append(self.start)
        return self.path_list


    def reset(self):
        for tile_no in self.tile_dict:
            self.tile_dict[tile_no].reset_for_AStar()

        self.start = 0
        self.target = 0
        self.closed_list = []
        self.open_list = []
        self.path_list = []
        self.LFT = 0

class TestAStar(unittest.TestCase):
    def setUp(self):
        self.test_map = map_class.LevelMap()
        self.test_map.initialize_tiles()
        self.test_astar = A_Star()
        self.test_astar.init_AStar(self.test_map.return_dict_of_tiles(), 1,100)

    def testSurroundingTiles(self):
        self.assertEquals(self.test_astar.get_surrounding_tiles(1), [11,2],
                            "Incorrect surrounding tiles for center tile {0} - we see: {1}".format(1, self.test_astar.get_surrounding_tiles(1)))
        self.assertEquals(self.test_astar.get_surrounding_tiles(5), [15,6,4],
                            "Incorrect surrounding tiles for center tile {0} - we see: {1}".format(5, self.test_astar.get_surrounding_tiles(5)))
        self.assertEquals(self.test_astar.get_surrounding_tiles(10), [20,9],
                            "Incorrect surrounding tiles for center tile {0} - we see: {1}".format(10, self.test_astar.get_surrounding_tiles(10)))
        #self.assertEquals(self.test_astar.get_surrounding_tiles(51), [61, 52, 41],
                            #"Incorrect surrounding tiles for center tile {0} - we see: {1}".format(51, self.test_astar.get_surrounding_tiles(51)))
        self.assertEquals(self.test_astar.get_surrounding_tiles(55), [65,56,45,54],
                            "Incorrect surrounding tiles for center tile {0} - we see: {1}".format(55, self.test_astar.get_surrounding_tiles(55)))
        self.assertEquals(self.test_astar.get_surrounding_tiles(60), [70, 50, 59],
                            "Incorrect surrounding tiles for center tile {0} - we see: {1}".format(60, self.test_astar.get_surrounding_tiles(60)))
        self.assertEquals(self.test_astar.get_surrounding_tiles(91), [92,81],
                            "Incorrect surrounding tiles for center tile {0} - we see: {1}".format(91, self.test_astar.get_surrounding_tiles(91)))
        self.assertEquals(self.test_astar.get_surrounding_tiles(95), [96,85,94],
                            "Incorrect surrounding tiles for center tile {0} - we see: {1}".format(95, self.test_astar.get_surrounding_tiles(95)))
        self.assertEquals(self.test_astar.get_surrounding_tiles(100), [90,99],
                            "Incorrect surrounding tiles for center tile {0}, seeing:  - we see: {1}".format(100, self.test_astar.get_surrounding_tiles(100)))
        self.test_astar.reset()


    def testPath(self):
        self.test_astar.init_AStar(self.test_map.return_dict_of_tiles(), 1,100)
        self.test_astar.run_AStar(self.test_astar.start)
        #self.assertEquals(self.test_astar.get_path(), [100, 99, 98, 97, 96,95,94,93,92,91,81,71,61,51,41,31,21,11,1], "AStar doesn't return accurate path, going from 1 to 100")
        self.test_astar.reset()

        self.test_astar.init_AStar(self.test_map.return_dict_of_tiles(), 1,91)
        self.test_astar.run_AStar(self.test_astar.start)
        self.assertEquals(self.test_astar.get_path(), [91,81,71,61,51,41,31,21,11,1], "AStar doesn't return accurate path, going from 1 to 91")
        self.test_astar.reset()

        self.test_astar.init_AStar(self.test_map.return_dict_of_tiles(), 10,1)
        self.test_astar.run_AStar(self.test_astar.start)
        self.assertEquals(self.test_astar.get_path(), [1,2,3,4,5,6,7,8,9,10], "AStar doesn't return accurate path, going from 10 to 1")


if __name__ == '__main__':
    unittest.main()
