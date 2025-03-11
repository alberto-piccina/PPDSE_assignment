from collections import Counter as Cnt

class Trainer:
    def __init__(self, name):
        self.name = name
        self.pokemon_list = []
        self.items = []
    
    # method to add an item in the bag
    def add_item(self, item):
        self.items.append(item)
        
    # method to use an item, only if it is present inside the bag
    def use_item(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print(item, ": Item not found!")
       
    # method to check the items inside the bag  
    def check_bag(self):
        items_number = len(self.items)
        print("\n", self.name, "has", items_number, "items in the bag:")
        count = Cnt(self.items)
        for item, frequency in count.items():
            print("->", item, "x", frequency)
            
    # method to add a pokemon in the team
    def add_pokemon(self, pokemon):
        if len(self.pokemon_list) < 6:
            self.pokemon_list.append(pokemon)
            print(pokemon.name, "has been added to", self.name,"'s team!")
        else:
            print(self.name, ", there is no more space in your team!")
            
    # method to remove a pokemon to the team
    def remove_pokemon(self, pokemon):
        if pokemon in self.pokemon_list:
            self.pokemon_list.remove(pokemon)
        else:
            print(pokemon.name, "is not in", self.name, "'s team!")
    
    # method to check the pokemon team
    def check_team(self):
        pokemon_number = len(self.pokemon_list)
        print("\n", self.name, "'s team is composed by", pokemon_number, "Pokemon:\n")
        for i in self.pokemon_list:
            print(i.name, "   ", "Lv.", i.level)