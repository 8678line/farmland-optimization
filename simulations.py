from nutrient_game import nutrient_game_grid
from crop_game import crop_game_grid
from simulate_nutrients import simulate_nutrients
from simulate_crops import simulate_crops
import numpy as np
import matplotlib.pyplot as plt

TAPs = {0: "random",
        1: "alternate_rows",
        2: "alternate_columns"}
def run_simulation_1():
    num_experiments = 100
    simulation_array = np.linspace(1, num_experiments, num_experiments)
    environment = crop_game_grid(rows = 10, columns = 10, num_crops = 10, TAP = TAPs[0])
    reward_list_1 = simulate_crops(environment, num_experiments)
    
    environment = crop_game_grid(rows = 10, columns = 5, num_crops = 6, TAP = TAPs[1])
    reward_list_2 = simulate_crops(environment, num_experiments)

    environment = crop_game_grid(rows = 3, columns = 12, num_crops = 20, TAP = TAPs[2])
    reward_list_3 = simulate_crops(environment, num_experiments)
    
    plt.plot(simulation_array, reward_list_1)
    plt.plot(simulation_array, reward_list_2)
    plt.plot(simulation_array, reward_list_3)
    
    plt.xlabel("experiment number")
    plt.ylabel("accuracy")
    plt.legend(["TAP 0", "TAP 1", "TAP 2"])
    plt.show()

'''
run one of the following algorithms and evaluate the average reward over n trials
    0: random agent
    1: hardcoded agent
    2: reactive agent
    3: deep reinforcement learning agent
'''
def run_simulation_2():
    num_trials = 30
    simulation_days = 100
    simulation_array = np.linspace(1, num_trials, num_trials)
    environment = nutrient_game_grid(simulation_days)

    reward_list_random = simulate_nutrients(environment, 0, num_trials, simulation_days)
    plt.plot(simulation_array, reward_list_random)
    print(f"random agent finished simulation with final average reward {reward_list_random[-1]}")
    
    reward_list_hardcoded = simulate_nutrients(environment, 1, num_trials, simulation_days)
    plt.plot(simulation_array, reward_list_hardcoded)
    print(f"hardcoded agent finished simulation with final average reward {reward_list_hardcoded[-1]}")
    
    reward_list_reactive = simulate_nutrients(environment, 2, num_trials, simulation_days)
    plt.plot(simulation_array, reward_list_reactive)
    print(f"reactive agent finished simulation with final average reward {reward_list_reactive[-1]}")
    
    reward_list_DRL = simulate_nutrients(environment, 3, num_trials, simulation_days)
    plt.plot(simulation_array, reward_list_DRL)
    print("DRL agent finished simulation")
    
    plt.xlabel("trial number")
    plt.ylabel(f"average cost per day during the {simulation_days} period")
    plt.legend(["random agent", "hardcoded agent", "reactive agent", "DRL agent"])
    plt.show()

if __name__ == '__main__':
    run_simulation_1()
    run_simulation_2()