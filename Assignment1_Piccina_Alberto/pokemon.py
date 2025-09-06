import math
import random
import copy

class Pokemon:
    def __init__(self,
                 name = "",
                 national_pokedex_number = 0,
                 types = None,
                 baseStats = None,
                 moves = None):
        self.name = name
        self.nickname = self.name
        self.national_pokedex_number = national_pokedex_number
        self.level = 1
        self.types = types if types is not None else []
        self.baseStats = baseStats if baseStats is not None else {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "speed": 0,
            "special": 0}
        self.curr_HP = self.baseStats["hp"]
        self.able_to_fight = True
        self.moves = copy.deepcopy(moves) if moves is not None else {}
        
        # setting a limit in the number of moves
        __max_number_moves = 4
        if (len(self.moves) > __max_number_moves):
            for i in range(len(moves)-1, __max_number_moves-1, -1):
                self.moves.pop(i)
        
    # method to use a certain move
    def useMove(self, move, other):
        if self.able_to_fight:
            if move["pp"] == 0:
                print(move["name"], "PP are zero, so", self.name, "can not use this move.")
            else:
                if other.able_to_fight:
                    move["pp"] -= 1
                    print("\n", self.nickname, "used", move["name"], "! (PP left over:", move["pp"], ")")
                    probability = random.random()
                    if probability < move["accuracy"]:
                        
                        # set attack value
                        if move["category"] == "physical":
                            attack = self.baseStats["attack"]
                        else:
                            attack = self.baseStats["special"]
                        
                        # set defense value
                        if move["category"] == "physical":
                            defense = other.baseStats["defense"]
                        else:
                            defense = other.baseStats["special"]
                        
                        # set stability
                        if move["type"] in self.types:
                            stability = 1.5
                        else:
                            stability = 1
                        
                        # set effect value, always equal to 1
                        effect = 1
                        
                        # set critical value
                        if probability < self.baseStats["speed"] / 512:
                            critical = 2
                            print("Critical Hit!")
                        else:
                            critical = 1
                        
                        # set luck value
                        epsilon = 1e-10
                        luck = random.uniform(0.85, 1 - epsilon)
                        
                        # damage computation
                        modifier = stability * effect * critical * luck
                        damage = int(math.floor(((2 * self.level + 10) / 250) * (attack / defense) * move["power"] + 2) * modifier)
                        other.curr_HP -= damage
                        
                        print(move["name"], "hit!", self.nickname, "did", damage, "damages!", 
                            other.nickname, "goes from", other.curr_HP + damage, "HP to", other.curr_HP, "HP!\n")
                        
                        if other.curr_HP <= 0:
                            print("Oh no!", other.nickname, "is out of fight!")
                            other.able_to_fight = False
                    
                    else:
                        print(move["name"], "missed!")
                else:
                    print("You can not attack", other.nickname, "because it is not able to fight.")
        else:
            print("You can not attack with", self.nickname, "because it is not able to fight.")
                
    # method to use a random move
    def useRandomMove(self, other):
        if other.able_to_fight:
            move = random.choice(list(self.moves.values()))
            if move["pp"] == 0:
                print(move["name"], "PP are zero, so", self.name, "can not use this move.")
            else:
                self.useMove(move, other)
        else:
            print("You can not attack", other.name, "because it is not able to fight.")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    # method to use a move from the pokemon's moveset
    # def useMove(self, move, other):
    #     if (move.pp == 0):
    #         print(move.name, "PP are zero, so", self.name, "can not use this move.")
    #     else:
    #         if (other.able_to_fight):
    #             move.pp -= 1
    #             print(self.name, "used", move.name, "! (PP left over:", move.pp, ")")
    #             probability = random.random()
    #             if (probability < move.accuracy):
                
    #                 # set attack value
    #                 if (move.category == "physical"):
    #                     attack = self.baseStats["attack"]
    #                 else:
    #                     attack = self.baseStats["special"]
                    
    #                 # set defense value
    #                 if (move.category == "physical"):
    #                     defense = other.baseStats["defense"]
    #                 else:
    #                     defense = other.baseStats["special"]
                    
    #                 # set stability
    #                 if (move.type in self.types):
    #                     stability = 1.5
    #                 else:
    #                     stability = 1
                    
    #                 # set effect value, always equal to 1
    #                 effect = 1
                    
    #                 # set critical value
    #                 if (probability < self.baseStats["speed"]/512):
    #                     critical = 2
    #                     print("Critical Hit!")
    #                 else:
    #                     critical = 1
                    
    #                 # set luck value
    #                 epsilon = 1e-10
    #                 luck = random.uniform(0.85,1-epsilon)
                    
    #                 # damage computation
    #                 modifier = stability * effect * critical * luck
    #                 damage = math.floor((( 2 * self.level + 10 )/(250) * ( attack / defense ) * move.power + 2) * modifier)
    #                 other.curr_HP -= damage
                    
    #                 print(move.name, "hit!" ,self.name, "did", damage, "damages!", other.name, "goes from", other.curr_HP+damage, "HP to", other.curr_HP, "HP! \n")
                    
    #                 if (other.curr_HP <= 0):
    #                     print("Oh no!", other.name, "is out of fight!")
    #                     other.able_to_fight = False
                
    #             else:
    #                 print(move.name, "missed!")
                    
    #         else:
    #             print("You can not attack", other.name, "because it is not able to fight.")
