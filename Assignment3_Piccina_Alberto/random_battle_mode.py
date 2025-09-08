import random
import pokemon_trainer

class GameEngine:
    def __init__(self, trainer, pokemon_list, moves_list, type_effectiveness_list):
        self.trainer = trainer
        self.pkmn_list = pokemon_list
        self.moves_list = moves_list
        self.type_effectiveness_list = type_effectiveness_list

    def run_automated_battles(self, num_battles):
        statistics = {
            "encountered_pokemons": [],
            "battle_outcomes": [], 
            "battle_turns": [],
            "residual_hp_percentage": []
        }

        player_pkmn = list(self.trainer.pokemon_list.values())[0]
        wild_trainer = pokemon_trainer.Trainer(name="Wild Trainer")

        for i in range(num_battles):
            wild_pokemon_name = random.choice([p["name"] for p in self.pkmn_list])
            wild_trainer.add_pokemon(self.pkmn_list, self.moves_list, wild_pokemon_name)
            wild_pkmn = list(wild_trainer.pokemon_list.values())[0]

            statistics["encountered_pokemons"].append(wild_pkmn.name)
            
            battle_turns = 0
            
            while player_pkmn.able_to_fight and wild_pkmn.able_to_fight:
                battle_turns += 1
                
                player_pkmn.useRandomMove(wild_pkmn, self.type_effectiveness_list, ignore_pp=True)

                if wild_pkmn.able_to_fight:
                    wild_pkmn.useRandomMove(player_pkmn, self.type_effectiveness_list, ignore_pp=True)

            statistics["battle_turns"].append(battle_turns)
            
            if player_pkmn.able_to_fight:
                statistics["battle_outcomes"].append("victory")
            else:
                statistics["battle_outcomes"].append("loss")
            
            if player_pkmn.able_to_fight:
                hp_percentage = (player_pkmn.curr_HP / player_pkmn.baseStats["hp"]) * 100
                statistics["residual_hp_percentage"].append(hp_percentage)
            else:
                statistics["residual_hp_percentage"].append(0)

            player_pkmn.heal()

            # To remove the random pkmn to the possible encounterable pokemon from the next steps
            wild_trainer.remove_pokemon(wild_pkmn.nickname)
        
        return statistics