import numpy as np
import random

#a crop game environment grid class
class game_grid():

    #a class for each tile on the grid
    class tile():
        def __init__(self, row, column):
            self.row = row #x position of tile
            self.column = column #y position of tile
            self.crop = None #is there a crop on this tile
            self.water = 10
            self.nutrients = {} #the nutrients in this tile, including pH
            self.tile_actions = {} #the actions available at this tile

        def print_tile(self):
            print(f'row: {self.row}, column: {self.column}\ncurrent crop: {self.crop}\nwater: {self.water}\nnutrients: {self.nutrients}\nactions: {self.tile_actions}\n')
    
    '''
    initialize the game grid with these parameters:
    rows:                   number of rows on the grid
    columns:                number of columns on the grid
    crop_list:              a list of crops available to plant on the grid
    simulation_days:        the number of days this environment will simulate for
    w_cost:                 the cost of applying water, in $/L
    '''
    def __init__(self, rows, columns, crop_list, simulation_days):
        #the grid size
        self.rows = rows
        self.columns = columns

        #a list of tiles on this environment, one for each state coordinate
        self.tiles = {}
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                self.tiles[row_idx, col_idx] = self.tile(row_idx, col_idx)

        #the action space for this environment
        self.action_space = crop_list.copy()

        #assign possible actions to each tile
        for location, tile in self.tiles.items():
            planting = []
            for crop in crop_list:
                planting.append(crop)
            tile.tile_actions["planting"] = planting
            tile.tile_actions["management"] = ['wait', 'harvest']
        
        #add nutrients (kg) to the grid following a uniform distribution of integers
        for tile in self.tiles.values():
            tile.nutrients["N"] = random.randint(45, 50)
            tile.nutrients["P"] = random.randint(27, 32)
            tile.nutrients["K"] = random.randint(39, 44)

        #apply smoothing / 3x3 average pooling for all nutrients for each tile, rounded
        for location, tile in self.tiles.items():
            for nutrient in tile.nutrients.keys():                
                count, total = 0, 0
                for r in range (location[0] - 1, location[0] + 2):
                    for c in range (location[1] - 1, location[1] + 2):
                        if (r, c) in self.tiles.keys():
                            count += 1
                            total += self.tiles[r, c].nutrients[nutrient]
                tile.nutrients[nutrient] = total // count
        
        #the number of days to simulate this environment
        self.simulation_days = simulation_days

        #the cost of using nutrients ($/kg) and water ($/1000L)
        self.n_cost = 0.38
        self.p_cost = 0.43
        self.k_cost = 0.40
        self.w_cost = 3

        #generate a reward distribution (a gaussian distribution) for each crop as a function of time
        self.inputs = [np.linspace(0, self.simulation_days, self.simulation_days + 1)] * len(self.action_space)
        self.distributions = {}
        
        for i in range(len(self.action_space)):
            self.distributions[self.action_space[i][0]] = self.harvest_distribution(self.action_space[i][2], 10, self.inputs[i], self.action_space[i][3])
    
    #a helper function to generate crop yield distributions
    def harvest_distribution(self, harvest_time, width, indices, scale):
        density = []
        for x in indices:
            x_minus_mu = x - harvest_time
            exponent = - 0.5*(np.dot(x_minus_mu,1/width)**2)
            prob = 1/np.sqrt(2*np.pi*width)*np.exp(exponent)
            density.append(prob*scale)
        return density
    
    #add nutrients to a particular tile
    def add_nutrients(self, type, row, column, amount):
        if self.rows*column + row > len(self.tiles):
            return
        if amount < 0:
            return
        for location, tile in self.tiles.items():
            if location == (row, column):
                tile.nutrients[type] += amount
            if tile.nutrients[type] > 50 and type == "N":
                tile.nutrients[type] = 50
            elif tile.nutrients[type] > 32 and type == "P":
                tile.nutrients[type] = 32
            elif tile.nutrients[type] > 44 and type == "K":
                tile.nutrients[type] = 44
    
    #all tiles with crops currently planted will require nutrients
    def use_nutrients(self, n_amount, p_amount, k_amount):
        for tile in self.tiles.values():
            if tile.crop != None:
                tile.nutrients["N"] -= n_amount
                tile.nutrients["P"] -= p_amount
                tile.nutrients["K"] -= k_amount
            if tile.nutrients["N"] < 45:
                tile.nutrients["N"] = 45
            if tile.nutrients["P"] < 27:
                tile.nutrients["P"] = 27
            if tile.nutrients["K"] < 39:
                tile.nutrients["K"] = 39

    #add water to the specified location, with a reduced effect of surrounding tiles
    def add_water(self, row, column, amount):
        if self.rows*column + row > len(self.tiles):
            return
        if amount < 0:
            return
        #add water to the specified tile
        self.tiles[row, column].water += amount
        if self.tiles[row, column].water > 20:
            self.tiles[row, column].water = 20
    
    #all tiles with crops currently planted will require water
    def use_water(self, amount):
        for tile in self.tiles.values():
            if tile.crop != None:
                tile.water -= amount
                if tile.water < 10:
                    tile.water = 10
     
    #get the crop yield for a tile at a particular timestep
    def get_crop_yield(self, row, column, timestep):
        n_value = self.tiles[row, column].nutrients["N"]
        p_value = self.tiles[row, column].nutrients["P"]
        k_value = self.tiles[row, column].nutrients["K"]
        w_value = self.tiles[row, column].water

        factor = 1
        if n_value < 48:
            factor -= 0.1
        if p_value < 30:
            factor -= 0.1
        if k_value < 42:
            factor -= 0.1
        if w_value < 0:
            factor -= 0.7

        return self.distributions[self.tiles[row, column].crop][timestep] * factor #function of timestep and the tile parameters (water, npk, type of crop, number of bad days)
    
    #the reward for a tile is a function of the crop yield and the actions taken
    def get_reward(self, action, crop_yield, valid_planting = True):
        harvest_cost = 0
        if(action[1] == 1):
            harvest_cost = 1
        
        crop_cost = 0
        if valid_planting == True and 2 <= action[0] < 2 + len(self.action_space):
            crop_cost = self.action_space[action[0]-2][1]
        
        nutrient_costs = self.n_cost * action[2] + self.p_cost * action[3] + self.k_cost * action[4]
        water_cost = self.w_cost * action[5]

        return crop_yield - crop_cost - harvest_cost - nutrient_costs - water_cost
    
    '''
    take action for one time step on a specific tile
    the action is a 6-item list containing these items:
    - the timestep
    - crop management number (one of the following):
        0: do nothing (default)
        1: harvest the tile (only if crop != None)
        2 to N+1: plant crop 1 through N
    - nitrogen addition amount (kg)
    - phosphorus addition amount (kg)
    - potassium addition amount (kg)
    - water addition amount (L)
    '''
    #action should update the state (state transition) and return a reward
    def take_action(self, row, column, action):
        #update the tile's nutrient and water parameters
        self.add_nutrients("N", row, column, action[2])
        self.add_nutrients("P", row, column, action[3])
        self.add_nutrients("K", row, column, action[4])
        self.add_water(row, column, action[5])

        #all tiles with crops use nutrients and water
        self.use_nutrients(1, 0.1, 1)
        self.use_water(1)

        #do nothing for crop management
        if action[1] == 0:
            return self.get_reward(action, 0)

        #invalid harvest
        if self.tiles[row, column].crop == None and action[1] == 1:
            return self.get_reward(action, 0)
        
        #harvesting a crop
        if self.tiles[row, column].crop != None and action[1] == 1:
            crop_yield = self.get_crop_yield(row, column, action[0])
            self.tiles[row, column].crop = None
            return self.get_reward(action, crop_yield)
        
        #crop already exists, attempting to plant again
        if self.tiles[row, column].crop != None and action[1] >= 2:
            return self.get_reward(action, 0, False)
        
        #planting a crop
        if self.tiles[row, column].crop == None and action[1] >= 2:
            #invalid crop
            if action[1] >= 2 + len(self.action_space):
                pass
            #valid crop
            else:
                self.tiles[row, column].crop = self.action_space[action[1] - 2][0]
            return self.get_reward(action, 0)

    #print some information about the environment
    def print_env(self):
        print("environment size:", self.rows, "rows by", self.columns, "columns")
        print("simulation days:", self.simulation_days)
        print("environment actions:", self.action_space)
        print("environment tile information:")
        for tile in self.tiles.values():
            self.tile.print_tile(tile) 
        print("\n")