import numpy as np
import random

#a crop game environment grid class
class game_grid():

    #a class for each tile on the grid
    class tile():
        def __init__(self, row, column):
            self.row = row #x position of tile
            self.column = column #y position of tile
            self.active = False #is there a crop on this tile
            self.water = 0
            self.pH = None
            self.nutrients = {} #the nutrients in this tile
            self.actions = {} #the actions available at this tile

        def print_tile(self):
            print(f'row:{self.row}, column:{self.column}\nactive: {self.active}\nwater: {self.water}\npH: {self.pH}\nnutrients: {self.nutrients}\nactions: {self.actions}\n')
    
    #initialize the game grid
    def __init__(self, rows, columns, crops_available):
        #the grid size
        self.rows = rows
        self.columns = columns

        #a complete list of actions for this environment
        self.actions = crops_available

        #a list of states in the environment
        self.states = [i for i in range(self.rows*self.columns)]

        #a list of state coordinates (row, column)
        self.coordinates = []
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                self.coordinates.append([row_idx, col_idx])

        #a list of tiles on this environment, one for each state
        self.tiles = []
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                self.tiles.append(self.tile(row_idx, col_idx))

    def nutrient_smoothing(self.tiles):
        return tiles

    #add all the nutrients specified in a nutrient list to each tile on the grid
    #add according to a uniform distribution within a radius around min and max
    def init_nutrients(self, nutrient_list):
        for nutrient in nutrient_list:
            name, min, max, radius = nutrient[0], nutrient[1][0], nutrient[1][1], nutrient[1][2]
            for i in range(len(self.tiles)):
                self.tiles[i].nutrients[name] = random.uniform(min-radius, max+radius)
        nutrient_smoothing(self.tiles)
        return
    
    

    #you can add water to the specified location, with a reduced effect of surrounding tiles
    def add_water(self, row, column, amount):
        if self.rows*column + row > len(self.states):
            print("attempting to add water to invalid tile position")
            return
        if amount < 0:
            print("cannot remove water from a tile")
            return
        #add water to the specified tile
        self.tiles[self.rows*column + row].water += amount
        '''
        #add water to the surrounding tiles
        if self.rows*(column-1) + row-1 in self.states:
            self.tiles[self.rows*(column-1) + row-1].water += amount/5
        if self.rows*(column-1) + row in self.states:
            self.tiles[self.rows*(column-1) + row].water += amount/5
        if self.rows*(column-1) + row+1 in self.states:
            self.tiles[self.rows*(column-1) + row+1].water += amount/5

        for r in range (row - 1, row + 1):
            for c in range (column - 1, column + 1):
                if r != row or c != column:
                    self.tiles[self.rows*c + r].water += amount/5
        return
        '''
    
    #all tiles with crops currently planted will require water
    def use_water(self, amount):
        for i in range(len(self.tiles)):
            if self.tiles[i].active == True:
                self.tiles[i].water -= amount
        return
    
    def print_env(self):
        print("environment size:")
        print(self.rows, "by", self.columns)
        print("\n")
        print("environment actions:")
        print(self.actions)
        print("\n")
        print("environment states:")
        print(self.states)
        print("\n")
        print("environment coordinates:")
        print(self.coordinates)
        print("\n")
        print("environment tiles:")
        print(self.tiles)
        print("\n")
        print("environment tile information:")
        for tile in self.tiles:
            self.tile.print_tile(tile) 
        print("\n")

