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