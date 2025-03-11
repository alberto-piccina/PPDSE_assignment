import math
import random
import copy
import moves

class Pokemon:
    def __init__(self, name, national_pokedex_number, types, baseStats, moves):
        self.name = name
        self.national_pokedex_number = national_pokedex_number
        self.level = 1
        self.types = types
        self.baseStats = baseStats
        self.curr_HP = baseStats["hp"]
        self.moves = copy.deepcopy(moves)
        
        # setting a limit in the number of moves
        __max_number_moves = 4
        if (len(self.moves) > __max_number_moves):
            for i in range(len(moves)-1, __max_number_moves-1, -1):
                self.moves.pop(i)
        
    # method to use a move from the pokemon's moveset
    def useMove(self, move, other):
        if (move.pp == 0):
            print(move.name, "PP are zero, so", self.name, "can not use this move.")
        else:
            print(self.name, "used", move.name, "!")
            probability = random.random()
            if (probability < move.accuracy):
            
                # set attack value
                if (move.category == "physical"):
                    attack = self.baseStats["attack"]
                else:
                    attack = self.baseStats["special"]
                
                # set defense value
                if (move.category == "physical"):
                    defense = other.baseStats["defense"]
                else:
                    defense = other.baseStats["special"]
                
                # set stability
                if (move.type in self.types):
                    stability = 1.5
                else:
                    stability = 1
                
                # set effect value, always equal to 1
                effect = 1
                
                # set critical value
                if (probability < self.baseStats["speed"]/512):
                    critical = 2
                    print("Critical Hit!")
                else:
                    critical = 1
                
                # set luck value
                epsilon = 1e-10
                luck = random.uniform(0.85,1-epsilon)
                
                # damage computation
                modifier = stability * effect * critical * luck
                damage = math.floor((( 2 * self.level + 10 )/(250) * ( attack / defense ) * move.power + 2) * modifier)
                other.curr_HP -= damage
                
                print(move.name, "hit!" ,self.name, "did", damage, "damages!")
                print(other.name, "'s HP go to", other.curr_HP, "!")
                move.pp -= 1
            
            else:
                print(move.name, "missed!")
                move.pp -= 1
