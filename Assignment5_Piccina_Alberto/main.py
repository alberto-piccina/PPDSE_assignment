import random_battle_mode
import utils
import pokemon_trainer
import json
from tqdm import tqdm

def main():
    
    file_path = "simulation_results.json"
    
    pkmn_list = utils.load_pokemons("pokemons.json")
    moves_list = utils.load_filtered_moves("moves.json")
    type_effectiveness_list = utils.load_from_file("type_effectiveness.json")

    starters = ["bulbasaur", "charmander", "squirtle", "pikachu"]
    num_games = 1000
    num_battles = 200

    all_results = {}
    
    wild_pkmn_list = [p for p in pkmn_list if p["name"] not in starters]

    for starter_name in starters:
        print(f"\nStarting simulation for {starter_name.capitalize()}...")
        
        all_encountered_pokemons = []
        all_battle_outcomes = []
        all_battle_turns = []
        all_residual_hp_percentage = []
        all_turns_details = []

        pbar = tqdm(range(num_games),desc="Game", unit="game")

        for game in pbar:
            pbar.set_description(f"Game nr.{game+1}")
            trainer = pokemon_trainer.Trainer(name=f"Player_{starter_name}")
            trainer.add_pokemon(pkmn_list, moves_list, starter_name)
            
            engine = random_battle_mode.GameEngine(trainer, wild_pkmn_list, moves_list, type_effectiveness_list)
            
            simulation_results = engine.run_automated_battles(num_battles)

            all_encountered_pokemons.extend(simulation_results["encountered_pokemons"])
            all_battle_outcomes.extend(simulation_results["battle_outcomes"])
            all_battle_turns.extend(simulation_results["battle_turns"])
            all_residual_hp_percentage.extend(simulation_results["residual_hp_percentage"])
            all_turns_details.extend(simulation_results.get("turns_details", []))

        all_results[starter_name] = {
            "encountered_pokemons": all_encountered_pokemons,
            "battle_outcomes": all_battle_outcomes,
            "battle_turns": all_battle_turns,
            "residual_hp_percentage": all_residual_hp_percentage,
            "turns_details": all_turns_details,
            "total_battles_simulated": num_games * num_battles,
            "battles_per_game": num_battles
        }

        print(f"Simulation completed for {starter_name.capitalize()}.")

    with open("simulation_results.json", "w") as f:
        json.dump(all_results, f, indent=4)
        print("\nData saved in simulation_results.json")

if __name__ == "__main__":
    main()