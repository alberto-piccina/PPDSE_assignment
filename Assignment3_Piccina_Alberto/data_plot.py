import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import json

with open("simulation_results.json", "r") as f:
    results = json.load(f)
    
# First Plot
plt.figure(figsize=(10, 6))

for starter, data in results.items():
    outcomes = data["battle_outcomes"]
    total_battles = data["total_battles_simulated"]
    battles_per_game = data["battles_per_game"]
    victories = np.array([1 if outcome == "victory" else 0 for outcome in outcomes])
    
    num_games = int(total_battles / battles_per_game)
    
    # Now I have a matrix where each row is a game and each column is a battle
    victories_reshaped = victories.reshape(num_games, battles_per_game)
    
    cumulative_victories_per_game = np.cumsum(victories_reshaped, axis=1)       # axis=1 to sum in a row-wise manner
    avg_cumulative_victories = np.mean(cumulative_victories_per_game, axis=0)   # axis=0 to average column-wise)
    
    plt.plot(range(1, battles_per_game + 1), avg_cumulative_victories, label=starter.capitalize())
    
plt.xlabel("Number of Battles")
plt.ylabel("Average Cumulative Victories")
plt.title("Average Cumulative Victories vs Number of Battles")
plt.legend()
plt.grid(True)
plt.show()