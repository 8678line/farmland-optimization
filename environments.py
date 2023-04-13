import numpy as np
np.random.seed(1)

from Game_environment import game_grid

#the baseline environment with 1 state
def envronment_1():
    crop_list = ["potato", "corn", "wheat"]
    environment = game_grid(1, 1, crop_list)
    nutrient_list = [("N", [15, 20, 5]), ("P", [15, 20, 5]), ("K", [15, 20, 5])]
    environment.init_nutrients(nutrient_list)
    environment.add_water(0, 0, 999)
    environment.print_env()

def envronment_2():
    crop_list = ["potato", "corn", "wheat"]
    environment = game_grid(2, 3, crop_list)
    nutrient_list = [("N", [15, 20, 5]), ("P", [15, 20, 5]), ("K", [15, 20, 5])]
    environment.init_nutrients(nutrient_list)
    environment.print_env()

if __name__ == '__main__':
    envronment_1()
    envronment_2()