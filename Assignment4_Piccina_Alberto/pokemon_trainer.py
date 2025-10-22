from collections import Counter as Cnt
import copy
import pokemon
import random

class Trainer:
    def __init__(self, name=""):
        self.name = name
        self.pokemon_list = {}
        self.items = []
    
    # method to add an item in the bag
    def add_item(self, item, quantity=1):
        for i in range(quantity):
            self.items.append(item)
        
    # method to use an item, only if it is present inside the bag
    def use_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"\n{self.name} used {item}.")
        else:
            print(f"\n{self.name} --> {item}: Item not found!")
       
    # method to check the items inside the bag  
    def check_bag(self):
        items_number = len(self.items)
        print(f"\n{self.name} has {items_number} items in the bag:")
        count = Cnt(self.items)
        for item, frequency in count.items():
            print(f"-> {item} x{frequency}")

    def _get_valid_moves(self, pokemon_types, moves_list):
        valid_moves = []
        for move in moves_list:
            # The move is valid if its type is in the Pokemon's types or if it's a "normal" type
            if move["type"] in pokemon_types or move["type"] == "normal":
                valid_moves.append(move)
        return valid_moves
            
    # method to add a pokemon in the team
    def add_pokemon(self, list_of_pkmns, list_of_moves, pokemon_name, nickname=""):
        __max_pokemon = 6
        if (len(self.pokemon_list) < __max_pokemon):
            pokemon_list = copy.deepcopy(list_of_pkmns)
            moves_list = copy.deepcopy(list_of_moves)
            
            matched_pokemon = [p for p in pokemon_list if p["name"] == pokemon_name.lower()]
            
            if matched_pokemon:
                pokemon_data = matched_pokemon[0]
                
                # pick up to 4 valid moves from moves_list based on the Pokemon types.
                if "moves" not in pokemon_data or not pokemon_data["moves"]:
                    candidate_moves = self._get_valid_moves(pokemon_data.get("types", []), moves_list)
                    # take up the first 4 moves
                    # pokemon_move_names = [m["name"] for m in candidate_moves[:4]]
                    # take up 4 random moves
                    pokemon_move_names = [m["name"] for m in random.sample(candidate_moves, min(4, len(candidate_moves)))]
                else:
                    pokemon_move_names = pokemon_data["moves"]
                    
                empty_pokemon = pokemon.Pokemon(
                    name=pokemon_data["name"],
                    national_pokedex_number=pokemon_data["national_pokedex_number"],
                    types=pokemon_data["types"],
                    baseStats=pokemon_data["baseStats"],
                    moves=None
                )
                
                if nickname != "":
                    empty_pokemon.nickname = nickname
                else:
                    empty_pokemon.nickname = pokemon_name.lower()

                for move_name in pokemon_move_names:
                    matched_move = [m for m in moves_list if m["name"] == move_name]
                    if matched_move:
                        empty_pokemon.moves[move_name] = copy.deepcopy(matched_move[0])
                        empty_pokemon.moves[move_name]["max_pp"] = empty_pokemon.moves[move_name]["pp"]
                    else:
                        print(f"Move {move_name} not found!")
                
                self.pokemon_list[empty_pokemon.nickname] = empty_pokemon
            else:
                print(f"{pokemon_name} not found.")
        else:
            print(f"{self.name}, there is no more space in your team! You cannot add any Pokemon to your team.")
            
    # method to remove a pokemon to the team
    def remove_pokemon(self, pokemon):
        if pokemon in self.pokemon_list:
            del self.pokemon_list[pokemon]
            # print(f"{pokemon} is removed from {self.name}'s team!")
        else:
            print(f"{pokemon} is not in {self.name}'s team!")
    
    # method to check the pokemon team
    def check_team(self):
        pokemon_number = len(self.pokemon_list)
        print(f"\n{self.name}'s team is composed by {pokemon_number} Pokemon:")
        for i,k in self.pokemon_list.items():
            print(f"--> {i} ({k.name})     Lv. {k.level}     HP {k.curr_HP}" )
            for j,h in k.moves.items():
                print(f"    {j}'s PP = {h['pp']}")