from game_grid import game_grid
import numpy as np

def get_actions():
    n = [0, 1, 2]
    p = [0, 1, 2]
    k = [0, 1, 2]
    for nn in n:
        for pp in p:
            for kk in k:
                print([nn,pp,kk])
    '''
    for nutrient in range(nutrients = [np.random.randint(0, 5), np.random.randint(0, 5), np.random.randint(0, 5)])
    water = [np.random.randint(0, 10)]
    management = np.argmax(environment.take_action(tile[0], tile[1], [timestep] + [mgmt] + nutrients + water) for mgmt in range(len(environment.tiles[tile].tile_actions["management"])))
    action = [timestep] + [management] + nutrients + water
    '''

def simulate(environment, algorithm, num_trials):
    if algorithm == 0:
        reward = 0
        for i in range(num_trials):    
            timestep = 0
            while timestep < environment.simulation_days:
                for tile in environment.tiles:
                    management = [np.random.randint(2+len(environment.tiles[tile].tile_actions["planting"]))]
                    nutrients = [np.random.randint(0, 2), np.random.randint(0, 2), np.random.randint(0, 2)]
                    water = [np.random.randint(0, 2)]
                    action = [timestep] + management + nutrients + water
                    reward += environment.take_action(tile[0], tile[1], action)
                timestep += 1
        avg_reward = reward/num_trials
        return avg_reward
    if algorithm == 1:
        #initialize the q table, with 1 entry per simulation day
        Q = []
        for i in range(environment.simulation_days):
            mgmt = np.linspace(0,2+len(environment.action_space), 3+len(environment.action_space))
            n = np.linspace(0, 2, 3)
            p = np.linspace(0, 2, 3)
            k = np.linspace(0, 2, 3)
            water = np.linspace(0, 2, 3)

            combined = np.array(np.meshgrid(mgmt, n, p, k)).T.reshape(-1, 4)
            Q.append([(item, 0) for item in combined])
        
        for i in range(num_trials):    
            timestep = 0
            while timestep < environment.simulation_days:
                for tile in environment.tiles:
                    management = [np.random.randint(2+len(environment.tiles[tile].tile_actions["planting"]))]
                    nutrients = [np.random.randint(0, 2), np.random.randint(0, 2), np.random.randint(0, 2)]
                    water = [np.random.randint(0, 2)]
                    action = [timestep] + management + nutrients + water
                    reward = environment.take_action(tile[0], tile[1], action)
                timestep += 1
        #do the q learning and update rule here
        return avg_reward
crops = {0:("potato", 5, 105, 5),
         1:("corn", 10, 80, 10),
         2:("wheat", 15, 100, 15)} 

'''
for each simulation, generate a grid environment:
- specify the grid size (rows, columns)
- specify the crops available
- specify the simulation length

run one of the following algorithms and evaluate the average reward over n trials
0: agent selects random action at each timestep
1: q learning agent
'''
def run_simulation_1():
    crop_list = [crops[0], crops[1], crops[2]]
    environment = game_grid(rows=1, columns=1, crop_list=crop_list, simulation_days=100)
    n = 20
    avg_reward = simulate(environment, 0, n)
    print(f"average rewards for random agent after {n} trials:", avg_reward)

def run_simulation_2():
    crop_list = [crops[0], crops[1], crops[2]]
    environment = game_grid(rows=2, columns=2, crop_list=crop_list, simulation_days=100)
    num_trials = 20
    avg_reward = simulate(environment, 1, num_trials)
    print(f"average rewards for random agent after {num_trials} trials:", avg_reward)

if __name__ == '__main__':
    run_simulation_1()
    run_simulation_2()
    #get_actions()