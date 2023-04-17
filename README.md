# "Farmland Optimization" repository

game.py contains an initial pygame implementation of a farmland environment with a visual user interface

crop_game.py contains the crop allocation task environment

nutrient_game.py contains the nutrient control task environment

simulations.py runs multiple simulations on both environments: this is the user testing file

simulate_crops.py contains a simulation loop for the crop allocation task

simulate_nutrients.py contains a training loop for the nutrient control task along with baseline evaluations

DRL_agent.py implements the deep deterministic policy gradient (DDPG) algorithm
