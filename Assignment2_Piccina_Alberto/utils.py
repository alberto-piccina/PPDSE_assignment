import json

def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            pokemon_list = json.load(file)
            return pokemon_list
    except FileNotFoundError:
        print(f"File '{filename}' does not exist.")
        return []