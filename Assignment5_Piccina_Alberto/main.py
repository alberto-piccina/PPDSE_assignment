import random_battle_mode
import utils
import pokemon_trainer
import json
from tqdm import tqdm
import random
import pandas as pd

def main():
    
    file_path = "simulation_results.json"
    
    pkmn_list = utils.load_pokemons("pokemons.json")
    moves_list = utils.load_filtered_moves("moves.json")
    type_effectiveness_list = utils.load_from_file("type_effectiveness.json")

    num_games = 1000
    num_battles = 500

    all_results = {
        "games": [],
        "summary": {
            "num_games": num_games,
            "battles_per_game": num_battles,
            "total_battles": num_games * num_battles
        }
    }
    
    wild_pkmn_list = [p for p in pkmn_list]
    starters_used = []
    
    # List to hold all battle data for DataFrame
    battles_data = []
    
    print(f"\nStarting simulation for {num_games} games -> RANDOM STARTERS MODE")

    pbar = tqdm(range(num_games), desc="Game", unit="game")

    for game in pbar:
        # Choose a random starter for this game
        starter_name = random.choice([p["name"] for p in pkmn_list])
        starters_used.append(starter_name)
        
        pbar.set_description(f"Game {game+1} - Starter: {starter_name}")
        
        trainer = pokemon_trainer.Trainer(name=f"Player_Game{game+1}")
        trainer.add_pokemon(pkmn_list, moves_list, starter_name)
        
        engine = random_battle_mode.GameEngine(trainer, wild_pkmn_list, moves_list, type_effectiveness_list)
        
        simulation_results = engine.run_automated_battles(num_battles)

        # Save the results of this specific game
        game_data = {
            "game_number": game + 1,
            "starter": starter_name,
            "player_pokemon": simulation_results["player_pokemon"],
            "encountered_pokemons": simulation_results["encountered_pokemons"],
            "battle_outcomes": simulation_results["battle_outcomes"],
            "battle_turns": simulation_results["battle_turns"],
            "residual_hp_percentage": simulation_results["residual_hp_percentage"],
            "turns_details": simulation_results.get("turns_details", []),
            "num_battles": num_battles
        }
        
        all_results["games"].append(game_data)
        
        player_pkmn = simulation_results["player_pokemon"]
        
        for battle_idx in range(num_battles):
            opponent_pkmn = simulation_results["encountered_pokemons"][battle_idx]
            
            battle_row = {
                "game_number": game + 1,
                "battle_number": battle_idx + 1,
                
                # Player Pokemon features
                "player_name": player_pkmn["name"],
                "player_type1": player_pkmn["types"][0] if len(player_pkmn["types"]) > 0 else None,
                "player_type2": player_pkmn["types"][1] if len(player_pkmn["types"]) > 1 else None,
                "player_hp": player_pkmn["actStats"]["hp"],
                "player_attack": player_pkmn["actStats"]["attack"],
                "player_defense": player_pkmn["actStats"]["defense"],
                "player_special": player_pkmn["actStats"]["special"],
                "player_speed": player_pkmn["actStats"]["speed"],
                
                # Opponent Pokemon features
                "opponent_name": opponent_pkmn["name"],
                "opponent_type1": opponent_pkmn["types"][0] if len(opponent_pkmn["types"]) > 0 else None,
                "opponent_type2": opponent_pkmn["types"][1] if len(opponent_pkmn["types"]) > 1 else None,
                "opponent_hp": opponent_pkmn["actStats"]["hp"],
                "opponent_attack": opponent_pkmn["actStats"]["attack"],
                "opponent_defense": opponent_pkmn["actStats"]["defense"],
                "opponent_special": opponent_pkmn["actStats"]["special"],
                "opponent_speed": opponent_pkmn["actStats"]["speed"],
                
                # Battle outcome
                "outcome": simulation_results["battle_outcomes"][battle_idx],
                "turns": simulation_results["battle_turns"][battle_idx],
                "residual_hp_percentage": simulation_results["residual_hp_percentage"][battle_idx]
            }
            
            battles_data.append(battle_row)

    print(f"\nSimulation completed.")
    print(f"\nStarters used in the games:")
    for i, starter in enumerate(starters_used, 1):
        print(f"  Game {i}: {starter.capitalize()}")

    # Save the JSON
    with open("simulation_results.json", "w") as f:
        json.dump(all_results, f, indent=4)
        print("\nData saved in simulation_results.json")
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(battles_data)
    df.to_csv("battles_dataframe.csv", index=False)
    print(f"DataFrame saved in battles_dataframe.csv with {len(df)} battles")
    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

if __name__ == "__main__":
    main()