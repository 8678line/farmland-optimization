import numpy as np

#simulate the crop distribution problem
def simulate_crops(environment, num_experiments):

    #the number of crops to simulate
    num_crops = environment.num_crops
    num_trials = 50
    reward_list = []

    for _ in range(num_experiments):
        scores = {}
        for location in environment.tiles.keys():
            scores[location] = 0

        for j in range(num_trials):
            for location, tile in environment.tiles.items():
                r = np.random.random(size=1)
                if r < tile.epsilon:
                    crop = np.random.randint(0, num_crops)
                else:
                    crop = tile.avg_reward.index(max(tile.avg_reward))
                reward = environment.get_reward(location[0], location[1], crop)
                scores[location] += reward

                tile.epsilon = 1/(j+1)
                tile.times_planted[crop] += 1
                tile.avg_reward[crop] += (reward - tile.avg_reward[crop]) / tile.times_planted[crop]


        for location, tile in environment.tiles.items():
            scores[location] /= num_trials
            scores[location] /= max(tile.reward.values())
        
        total_score = np.array(list(scores.values())).mean()
        reward_list.append(total_score)
                  
    return reward_list