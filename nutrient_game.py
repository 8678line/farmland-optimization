import numpy as np

#a game environment grid for nutrient optimization
class nutrient_game_grid():
    def __init__(self, simulation_days):
        self.N = np.random.uniform(50, 55)
        self.P = np.random.uniform(32, 37)
        self.K = np.random.uniform(44, 49)
        self.water = np.random.uniform(10, 15)
        
        self.simulation_days = simulation_days

        #the cost of using nutrients and water
        self.N_cost = 0.09802
        self.P_cost = 0.06693
        self.K_cost = 0.02365
        self.water_cost = 0.0279
  
    #penalize the agent if the environment conditions fall below an optimal level
    def get_penalty(self):
        penalty = 0
        if self.N < 48:
            penalty += (48 - self.N)**1.3
        elif self.N > 80:
            penalty += (self.N - 80)**1.3
        if self.P < 30:
            penalty += (30 - self.P)**1.3
        elif self.P > 62:
            penalty += (self.P - 62)**1.3
        if self.K < 42:
            penalty += (42 - self.K)**1.3
        elif self.K > 74:
            penalty += (self.K - 74)**1.3
        if self.water < 8:
            penalty += (8 - self.water)**1.3
        elif self.water > 40:
            penalty += (self.water - 40)**1.3
        return penalty
    
    #use resources each day
    def use_resources(self):
        self.N -= 1
        self.P -= 1
        self.K -= 1
        self.water -= 1
    
    '''
    the action is a 4-item list containing these items:
    - the amount of nitrogen used (m^2)
    - the amount of phosphorus used (m^2)
    - the amount of potassium used (m^2)
    - the amount of water used (m^2)
    '''
    #action should update the state (state transition) and return a reward
    def take_action(self, action):
        #update the tile with the resource amounts
        self.N += action[0]
        self.P += action[1]
        self.K += action[2]
        self.water += action[3]
        resource_cost = action[0]*self.N_cost + action[1]*self.P_cost + action[2]*self.K_cost + action[3]*self.water_cost

        labor_cost = 0
        #if at lease one resource is applied, there is a labor cost
        #this encourages the agent to use resources less frequently, but more resources each time
        if np.count_nonzero(action) > 0:
            labor_cost = 3

        self.use_resources()
        resource_penalty = self.get_penalty()
        
        return - resource_cost - resource_penalty - labor_cost
    
    #reset the grid tiles
    def reset(self):
        self.N = np.random.uniform(50, 55)
        self.P = np.random.uniform(32, 37)
        self.K = np.random.uniform(44, 49)
        self.water = np.random.uniform(10, 15)

        state = [self.N, self.P, self.K, self.water]
        return state, 0, False
