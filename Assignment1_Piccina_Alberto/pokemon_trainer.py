from collections import Counter as Cnt
import copy
import pokemon

class Trainer:
    def __init__(self, name):
        self.name = name
        self.pokemon_list = {}
        self.items = []
    
    # method to add an item in the bag
    def add_item(self, item):
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
            
    # method to add a pokemon in the team
    def add_pokemon(self, list_of_pkmns, list_of_moves, pokemon_name, nickname=""):
        __max_pokemon = 6
        if (len(self.pokemon_list) < __max_pokemon):
            pokemon_list = copy.deepcopy(list_of_pkmns)
            moves_list = copy.deepcopy(list_of_moves)
            result = [pokemon for pokemon in pokemon_list if pokemon["name"] == pokemon_name]
            empty_pokemon = pokemon.Pokemon()
            
            if result:
                index = pokemon_list.index(result[0])
                empty_pokemon.name = pokemon_list[index]["name"]
                empty_pokemon.nickname = nickname if nickname != "" else empty_pokemon.name
                empty_pokemon.national_pokedex_number = pokemon_list[index]["national_pokedex_number"]
                empty_pokemon.types = pokemon_list[index]["types"]
                empty_pokemon.baseStats = pokemon_list[index]["baseStats"]
                empty_pokemon.curr_HP = empty_pokemon.baseStats["hp"]
                empty_pokemon.moves = pokemon_list[index]["moves"]
                
                for move_name in empty_pokemon.moves.keys():
                    matched_move = [move for move in moves_list if move["name"] == move_name]
                    if matched_move:
                        empty_pokemon.moves[move_name] = copy.deepcopy(matched_move[0])
                    else:
                        print(f"Move {move_name} not found!")
                
                self.pokemon_list[empty_pokemon.nickname] = empty_pokemon
                print(f"{empty_pokemon.nickname} ({empty_pokemon.name}) has been added to {self.name}'s team!")
                
            else:
                print(f"{pokemon_name} not found.")
        else:
            print(f"{self.name}, there is no more space in your team! You cannot add any Pokemon to your team.")
            
    # method to remove a pokemon to the team
    def remove_pokemon(self, pokemon):
        if pokemon in self.pokemon_list:
            del self.pokemon_list[pokemon]
            print(f"{pokemon} is removed from {self.name}'s team!")
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