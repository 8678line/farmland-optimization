# "Farmland Optimization" repository

This project contains two tasks, both implemented in python using reinforcement learning and/or other machine learning techniques.

1. Crop allocation: the agent's goal is to spatially distribute a set of crops to achieve the maximum award, where each crop placement returns a reward depending on the location is it planted.

2. Nutrient control: the agent's goal is to minimize the average daily nutrient and water spending throughout a growing season.


Below are the python files involved in this project:

game.py contains an initial pygame implementation of a farmland environment with a functional user interface

crop_game.py contains the crop allocation task environment.

nutrient_game.py contains the nutrient control task environment.

simulations.py runs multiple simulations on both environments: this is the user testing file

simulate_crops.py contains a simulation loop for the crop allocation task

simulate_nutrients.py contains a training loop for the nutrient control task along with baseline evaluations

DRL_agent.py implements the deep deterministic policy gradient (DDPG) algorithm
