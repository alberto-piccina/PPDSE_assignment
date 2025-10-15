import json
import pandas as pd

def load_from_file(filename):
    try:
        data_list = []
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    data_list.append(json.loads(line))
        return data_list
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: file '{filename}' contains invalid JSON format.")
        return []

def load_filtered_moves(filename):
    moves = load_from_file(filename)
    filtered_moves = []
    for move in moves:
        # Filter only moves that have a 'power' attribute
        if move.get('power') is not None:
            # Do not consider 'effect', 'effects', and 'changes' attributes
            move_copy = {key: value for key, value in move.items() if key not in ["effect", "effects", "changes"]}
            filtered_moves.append(move_copy)
            
    moves_df = pd.DataFrame(filtered_moves)
    return moves_df

def load_type_effectiveness(filename):
    types = load_from_file(filename)
    types_df = pd.DataFrame(types)
    return types_df

def load_pokemons(filename):
    pokemons = load_from_file(filename)
    for pokemon in pokemons:
        pokemon['level'] = 1 # Set default level to 1
    pokemons_df = pd.DataFrame(pokemons)
    return pokemons_df