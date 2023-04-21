import numpy as np
import matplotlib.pyplot as plt

#a game environment grid for crop spatial allocation
class crop_game_grid():
    class tile():
        def __init__(self, row, column, num_crops):
            self.row = row
            self.column = column
            self.reward = {}
            self.epsilon = 1
            self.times_planted = np.array([0 for _ in range(num_crops)])
            self.avg_reward = [0] * num_crops
            self.reward_hist = [[]] * num_crops

        def print_tile(self):
            print(f"row {self.row} column {self.column}\nepsilon {self.epsilon}\ntimes_planted {self.times_planted}\naverage_reward {self.avg_reward}")
    
    '''
    initialize the game grid with these parameters:
    rows:       number of rows on the grid
    columns:    number of columns on the grid
    crop_list:  a list of crops available to plant on the grid, along with their reward distributions
    '''
    def __init__(self, rows, columns, num_crops, TAP):
        #the grid size
        self.rows = rows
        self.columns = columns
        self.num_crops = num_crops

        #a list of tiles on this environment, one for each state coordinate
        self.tiles = {}
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                self.tiles[row_idx, col_idx] = self.tile(row_idx, col_idx, self.num_crops)

        self.TAP = TAP
        self.init_probabilities(TAP)
        

    #initialize the probability distributions for each crop on the grid
    def init_probabilities(self, TAP):
        if TAP == "random":
            for tile in self.tiles.values():
                for i in range(self.num_crops):
                    tile.reward[i] = np.random.uniform()
        
        elif TAP == "alternate_rows":
            reward_list = np.zeros([self.rows,1])
            for i in range(self.rows):
                reward_list[i] = (i%self.num_crops)
                for location, tile in self.tiles.items():
                    for i in range(self.num_crops):
                        if i == reward_list[location[0]]:
                            tile.reward[i] = np.random.uniform(0.5, 1)
                        else:
                            tile.reward[i] = np.random.uniform(0, 0.5)
        
        elif TAP == "alternate_columns":
            reward_list = np.zeros([1,self.columns])
            for i in range(self.columns):
                reward_list[0][i] = (i%self.num_crops)
                for location, tile in self.tiles.items():
                    for i in range(self.num_crops):
                        if i == reward_list[0][location[1]]:
                            tile.reward[i] = np.random.uniform(0.5, 1)
                        else:
                            tile.reward[i] = np.random.uniform(0, 0.5)

    #return the reward for an action
    def get_reward(self, row, column, action):
        roll = np.random.random(size=1)
        if roll < self.tiles[row, column].reward[action]:
            return 1
        else:
            return 0
    
    #show the heatmap for the first crop
    def plot_grid(self):
        self.heatmap = np.zeros((self.rows, self.columns))
        for row in range(self.rows):
            for column in range(self.columns):
                self.heatmap[row][column] = self.tiles[row, column].reward[0]
        plt.imshow(self.heatmap)
        plt.show()
