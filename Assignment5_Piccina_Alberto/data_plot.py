import os
import matplotlib.pyplot as plt
import math
import numpy as np
import json
import collections
import collections

# Plots' Directory
output_dir = "PLOTS"
os.makedirs(output_dir, exist_ok=True)

with open("simulation_results.json", "r") as f:
    results = json.load(f)










    
# # First Plot
# # For each starter pokemon, display in the same graph the cumulative number of  victories 
# # over the Nbattles battles averaged across the Ngames games
# print("Plotting 1st graph")
# plt.figure(figsize=(10, 6))

# for starter, data in results.items():
#     outcomes = data["battle_outcomes"]
#     total_battles = data["total_battles_simulated"]
#     battles_per_game = data["battles_per_game"]
#     victories = np.array([1 if outcome == "victory" else 0 for outcome in outcomes])
    
#     num_games = int(total_battles / battles_per_game)
    
#     # Now I have a matrix where each row is a game and each column is a battle
#     victories_reshaped = victories[:num_games*battles_per_game].reshape(num_games, battles_per_game)
    
#     victories_per_game = victories_reshaped.sum(axis=1)
    
#     cumulative_victories = np.cumsum(victories_per_game)
    
#     plt.plot(range(1, num_games + 1), cumulative_victories, label=starter.capitalize())
    
# plt.xlabel("Number of Games")
# plt.ylabel("Average Cumulative Victories")
# plt.title("Average Cumulative Victories vs Number of Games")
# plt.legend()
# plt.grid(True)
# filename = "cum_victories_per_game.png"
# filepath = os.path.join(output_dir, filename)
# plt.savefig(filepath, dpi=300)
# plt.close()


# # Second Plot
# # 1. Display the distribution of  the number of  turns in each battle.
# # 2. Display the distribution of the residual player’s pokemon HPs at the end of each battle.
# # 3. Compute and show the distributions mean, median, 25th quartile and 75th quartile.

# all_turns = []
# all_hp = []

# for starter, data in results.items():
#     all_turns = data["battle_turns"]
#     all_hp.extend(data["residual_hp_percentage"])

# turns_median = np.median(all_turns)
# print("Plotting 2nd graph")

# plt.figure(figsize=(8, 6))
# plt.boxplot(all_turns, vert=False)
# plt.title("Distribution of the Number of Turns in each battle")
# plt.xlabel("Number of Turns")
# plt.text(0.05, 0.95, f"Mean: {np.mean(all_turns):.2f}\nMedian: {turns_median:.2f}\n25° Quartile: {np.percentile(all_turns, 25):.2f}\n75° Quartile: {np.percentile(all_turns, 75):.2f}",
#             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
# filename = "battle_turns_distribution.png"
# filepath = os.path.join(output_dir, filename)
# plt.savefig(filepath, dpi=300)
# plt.close()

# plt.figure(figsize=(8, 6))
# plt.boxplot(all_hp, vert=False)
# plt.title("Distribution of the Residual HPs")
# plt.xlabel("Residual HP's Percentage")
# plt.text(0.05, 0.95, f"Mean: {np.mean(all_hp):.2f}\nMedian: {np.median(all_hp):.2f}\n25° Quartile: {np.percentile(all_hp, 25):.2f}\n75° Quartile: {np.percentile(all_hp, 75):.2f}",
#             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
# filename = "residual_hp_distribution.png"
# filepath = os.path.join(output_dir, filename)
# plt.savefig(filepath, dpi=300)
# plt.close()


# # Bar charts (a graph for each starter pokemon)
# # 1. For each unique enemy pokemon encountered show the percentage of player’s victories.
# # 2. For each unique enemy pokemon encountered show the mean and standard deviation of  
# # the residual player’s pokemon HPs at the end of  each battle in the same graph
# num_blocks = 8
# subplots_per_fig = 4
# print("Plotting 3rd graph")
# # for each starter
# for starter, info in results.items():
#     print(f"    - Plotting for starter: {starter.capitalize()}")
    
#     # Collect data
#     enemies = info["encountered_pokemons"]
#     outcomes = info["battle_outcomes"]
#     hp_end = info["residual_hp_percentage"]

#     enemy_stats = {}
#     for enemy, outcome, hp in zip(enemies, outcomes, hp_end):
#         win = outcome in [True, "victory", "Victory", "win", "Win"]
#         if enemy not in enemy_stats:
#             enemy_stats[enemy] = {"wins": 0, "total": 0, "hp": []}
#         enemy_stats[enemy]["total"] += 1
#         if win:
#             enemy_stats[enemy]["wins"] += 1
#         enemy_stats[enemy]["hp"].append(hp)

#     enemy_names = sorted(enemy_stats.keys())
#     win_rates = [enemy_stats[e]["wins"] / enemy_stats[e]["total"] * 100 for e in enemy_names]
#     hp_means = [np.mean(enemy_stats[e]["hp"]) for e in enemy_names]
#     hp_stds = [np.std(enemy_stats[e]["hp"]) for e in enemy_names]

#     # Blocks
#     block_size = math.ceil(len(enemy_names) / num_blocks)
#     blocks = [enemy_names[i:i + block_size] for i in range(0, len(enemy_names), block_size)]

#     # Number of figures
#     num_figures = math.ceil(len(blocks) / subplots_per_fig)

#     for fig_idx in range(num_figures):
#         fig, axes = plt.subplots(2, 2, figsize=(15, 10))
#         axes = axes.flatten()
        
#         for subplot_idx in range(subplots_per_fig):
#             block_idx = fig_idx * subplots_per_fig + subplot_idx
#             if block_idx >= len(blocks):
#                 axes[subplot_idx].axis('off')
#                 continue
            
#             block = blocks[block_idx]
#             x = np.arange(len(block))
#             block_win_rates = [win_rates[enemy_names.index(e)] for e in block]
#             block_hp_means = [hp_means[enemy_names.index(e)] for e in block]
#             block_hp_stds = [hp_stds[enemy_names.index(e)] for e in block]

#             # Win Rate
#             axes[subplot_idx].bar(x - 0.2, block_win_rates, width=0.4, color='skyblue', edgecolor='black', label='Win Rate [%]')
#             axes[subplot_idx].set_ylabel('Win Rate [%]', color='blue')
#             axes[subplot_idx].set_ylim(0, 100)

#             # Res HP
#             ax2 = axes[subplot_idx].twinx()
#             ax2.bar(x + 0.2, block_hp_means, width=0.4, yerr=block_hp_stds, color='lightgreen', edgecolor='black', capsize=5, label='Residual HP [%]')
#             ax2.set_ylim(0, 100)
#             ax2.set_ylabel('Residual HP [%]', color='green')

#             axes[subplot_idx].set_xticks(x)
#             axes[subplot_idx].set_xticklabels(block, rotation=90, fontsize=8)
#             axes[subplot_idx].set_title(f'Enemies {block_idx*block_size +1}-{min((block_idx+1)*block_size,len(enemy_names))}')

#         plt.suptitle(f"{starter.capitalize()} - Battle Stats", fontsize=16)
#         plt.tight_layout(rect=[0, 0.03, 1, 0.95])
#         plt.grid(True)
#         filename = f"{starter}_figure{fig_idx+1}.png"
#         filepath = os.path.join(output_dir, filename)
#         plt.savefig(filepath, dpi=300)
#         plt.close(fig)
        
print(f"PLOT PROCESS COMPLETED!\nPlots available in directory '{output_dir}'.")

# ==================================================
# Simple Plot: average (± std) reduction of player's
# Pokemon HP percentage along battle turns
# ==================================================
print("\nPlotting HP reduction per turn (mean ± std) for each starter...")
plt.figure(figsize=(10, 6))

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']

for idx, (starter, data) in enumerate(results.items()):
    turns_data = data.get("turns_details", [])
    if not turns_data:
        continue

    # Reconstruct per-battle reduction sequences (in percent)
    per_battle_reductions = []
    player_nick = starter  # trainer.add_pokemon sets nickname to pokemon_name.lower()

    for battle in turns_data:
        if not battle:
            continue

        # determine starting HP from the first entry where attacker is player
        starting_hp = None
        for entry in battle:
            if entry.get("attacker") == player_nick:
                starting_hp = entry.get("attacker_hp_before")
                break
        # fallback: try to find any attacker_hp_before or defender_hp_after
        if starting_hp is None:
            if battle:
                starting_hp = battle[0].get("attacker_hp_before") or battle[0].get("defender_hp_after")
        if starting_hp in (None, 0):
            # skip malformed battle
            continue

        # current_hp represents the player's hp as we process events
        current_hp = starting_hp

        # collect hp at the end of each full turn
        turn_to_entries = {}
        for entry in battle:
            t = entry.get("turn")
            turn_to_entries.setdefault(t, []).append(entry)

        battle_reductions = []
        for t in sorted(turn_to_entries.keys()):
            for entry in turn_to_entries[t]:
                # if the player is the defender, update their hp after opponent's attack
                if entry.get("defender") == player_nick:
                    current_hp = entry.get("defender_hp_after", current_hp)
            # reduction percentage at end of this turn
            reduction_pct = (starting_hp - current_hp) / starting_hp * 100
            battle_reductions.append(reduction_pct)

        if battle_reductions:
            per_battle_reductions.append(battle_reductions)

    if not per_battle_reductions:
        continue

    # find max length
    max_len = max(len(seq) for seq in per_battle_reductions)

    # aggregate per turn
    mean_per_turn = []
    std_per_turn = []
    x = list(range(1, max_len + 1))
    for turn_idx in range(max_len):
        vals = [seq[turn_idx] for seq in per_battle_reductions if len(seq) > turn_idx]
        if vals:
            mean_per_turn.append(np.mean(vals))
            std_per_turn.append(np.std(vals))
        else:
            mean_per_turn.append(np.nan)
            std_per_turn.append(np.nan)

    mean_arr = np.array(mean_per_turn)
    std_arr = np.array(std_per_turn)

    color = colors[idx % len(colors)]
    plt.plot(x, mean_arr, label=starter.capitalize(), color=color)
    plt.fill_between(x, mean_arr - std_arr, mean_arr + std_arr, color=color, alpha=0.2)

plt.xlabel("Turn")
plt.ylabel("Average HP reduction [%]")
plt.title("Average (± std) reduction of player's Pokémon HP vs Turn")
plt.legend()
plt.grid(True)
filepath = os.path.join(output_dir, "hp_reduction_per_turn.png")
plt.tight_layout()
plt.savefig(filepath, dpi=300)
plt.close()
print(f"Saved HP reduction plot to {filepath}")



# Pie plots: for each starter, show (left) percentage usage of each attack and (right) percentage of total damage by each attack
for starter, data in results.items():
    turns_data = data.get("turns_details", [])
    if not turns_data:
        continue

    move_counts = collections.Counter()
    move_damage = collections.Counter()
    player_key = starter.lower()

    for battle in turns_data:
        if not battle:
            continue
        for entry in battle:
            attacker = (entry.get("attacker") or "").lower()
            if attacker != player_key:
                continue

            # extract move name
            move = None
            for k in ("move", "move_name", "attack", "action"):
                v = entry.get(k)
                if v:
                    move = v
                    break
            if isinstance(move, dict):
                move = move.get("name") or move.get("move") or str(move)
            if not move:
                move = "UNKNOWN"

            # extract damage (prefer explicit fields, otherwise compute from hp before/after)
            damage = None
            for dk in ("damage", "damage_dealt", "damage_amount", "hp_change"):
                if dk in entry and entry.get(dk) is not None:
                    try:
                        damage = float(entry.get(dk))
                        break
                    except Exception:
                        pass
            if damage is None:
                db = entry.get("defender_hp_before")
                da = entry.get("defender_hp_after")
                try:
                    if db is not None and da is not None:
                        damage = float(db) - float(da)
                except Exception:
                    damage = None
            if damage is None:
                damage = 0.0
            else:
                damage = max(0.0, float(damage))

            move_counts[move] += 1
            move_damage[move] += damage

    if not move_counts:
        continue

    # Order moves consistently (by usage desc)
    moves = [m for m, _ in move_counts.most_common()]
    counts = np.array([move_counts[m] for m in moves], dtype=float)
    damages = np.array([move_damage[m] for m in moves], dtype=float)

    # percentages
    total_counts = counts.sum()
    total_damage = damages.sum()
    usage_pct = counts / total_counts * 100 if total_counts > 0 else np.zeros_like(counts)
    damage_pct = damages / total_damage * 100 if total_damage > 0 else np.zeros_like(damages)

    # plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    colors = plt.cm.tab20.colors

    axes[0].pie(usage_pct, labels=moves, autopct="%1.1f%%", startangle=90, colors=colors[: len(moves)])
    axes[0].set_title(f"{starter.capitalize()} - Move usage (%)")

    axes[1].pie(damage_pct, labels=moves, autopct="%1.1f%%", startangle=90, colors=colors[: len(moves)])
    axes[1].set_title(f"{starter.capitalize()} - Damage contribution (%)")

    plt.suptitle(f"{starter.capitalize()} - Moves: usage vs damage", fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    filename = f"{starter}_moves_pie.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    print(f"Saved moves pie plot to {filepath}")