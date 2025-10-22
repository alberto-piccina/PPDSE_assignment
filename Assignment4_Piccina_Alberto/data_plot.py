import os
import matplotlib.pyplot as plt
import math
import numpy as np
import json
import collections
from utils import load_pokemons

# Plots' Directory
output_dir = "PLOTS"
os.makedirs(output_dir, exist_ok=True)

with open("simulation_results.json", "r") as f:
    results = json.load(f)


# Simple Plot: display the average HP reduction per turn (mean ± std) for each starter Pokémon
print("\nPlotting HP reduction per turn (mean ± std) for each starter...")
plt.figure(figsize=(10, 6))

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']

for idx, (starter, data) in enumerate(results.items()):
    turns_data = data.get("turns_details", [])
    if not turns_data:
        continue

    # Reconstruct per-battle reduction sequences (in percent)
    per_battle_reductions = []
    player_nick = starter

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

            # extract damage
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

    # Order moves
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



# Pie plot: full encounter distribution with legend on the right
all_encounters = []
for starter, info in results.items():
    all_encounters.extend(info.get("encountered_pokemons", []))

enc_counter = collections.Counter(all_encounters)

if not enc_counter:
    print("No encounters found — skipping encounter pie chart.")
else:
    # Sort all Pokémon by frequency
    sorted_encounters = enc_counter.most_common()
    labels = [name.capitalize() for name, _ in sorted_encounters]
    sizes = [count for _, count in sorted_encounters]

    # Pie chart
    fig, ax = plt.subplots(figsize=(16, 10))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5)
    )

    # Complete legend on the right
    legend_labels = [f"{label} ({count})" for label, count in zip(labels, sizes)]

    ax.legend(
        wedges,
        legend_labels,
        title="Encountered Pokémon",
        loc='center left',
        bbox_to_anchor=(1.05, 0.5),  # Legend on the right
        fontsize=8,
        title_fontsize=10,
        ncol=3,  # Columns in the legend
        frameon=False
    )

    ax.set_title("Distribution of All Encountered Pokémon", fontsize=14)
    ax.axis('equal')

    filename = "encounter_distribution_pie.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved full encounter distribution pie plot to {filepath}")

#  THE ABOVE PLOT WAS NOT REQUIRED, SO IT CAN BE REMOVED IF NEEDED



# Pie plot: display in the same figure the distribution of pokemon types in the pokemons.json file and the distribution of pokemon types in the list of pokemons encountered during the games
pokemons_data = load_pokemons("pokemons.json")

with open("simulation_results.json", "r") as f:
    simulation_results = json.load(f)

# Count types in the full pokemons.json dataset
all_types = []
for p in pokemons_data:
    all_types.extend(p.get("types", []))
type_counts_all = collections.Counter(all_types)

# Map from Pokemon name to its types
pokemon_type_map = {p["name"].lower(): p.get("types", []) for p in pokemons_data}

# Extract all encountered Pokémon from simulation results
encountered_pokemons = []
for starter, data in simulation_results.items():
    encountered_pokemons.extend(data.get("encountered_pokemons", []))

# Count types of encountered Pokémon
encountered_types = []
for name in encountered_pokemons:
    types = pokemon_type_map.get(name.lower(), [])
    encountered_types.extend(types)
type_counts_encountered = collections.Counter(encountered_types)

# Plots
fig, axs = plt.subplots(1, 2, figsize=(14, 7))
colors = plt.cm.tab20.colors  # 20 colors

# Pie 1
axs[0].pie(
    type_counts_all.values(),
    labels=type_counts_all.keys(),
    autopct="%1.1f%%",
    startangle=90,
    colors=colors[:len(type_counts_all)],
)
axs[0].set_title("Pokémon Types in pokemons.json")

# Pie 2
axs[1].pie(
    type_counts_encountered.values(),
    labels=type_counts_encountered.keys(),
    autopct="%1.1f%%",
    startangle=90,
    colors=colors[:len(type_counts_encountered)],
)
axs[1].set_title("Pokémon Types Encountered During Games")

plt.suptitle("Comparison of Pokémon Type Distributions", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the figure
filepath = os.path.join(output_dir, "pokemon_type_distribution_comparison.png")
plt.savefig(filepath, dpi=300)
print(f"Saved type distribution comparison plot to {filepath}")


print(f"PLOT PROCESS COMPLETED!\nPlots available in directory '{output_dir}'.")
