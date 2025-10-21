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
            "player_pokemon": [],
            "encountered_pokemons": [],
            "battle_outcomes": [], 
            "battle_turns": [],
            "residual_hp_percentage": [],
            "turns_details": []
        }

        player_pkmn = list(self.trainer.pokemon_list.values())[0]
        
        statistics["player_pokemon"] = {
            "name": player_pkmn.name,
            "level": player_pkmn.level,
            "types": player_pkmn.types,
            "actStats": player_pkmn.actStats
        }
        
        wild_trainer = pokemon_trainer.Trainer(name="Wild Trainer")

        for i in range(num_battles):
            wild_pokemon_name = random.choice([p["name"] for p in self.pkmn_list])
            wild_trainer.add_pokemon(self.pkmn_list, self.moves_list, wild_pokemon_name)
            wild_pkmn = list(wild_trainer.pokemon_list.values())[0]

            statistics["encountered_pokemons"].append({
                "name": wild_pkmn.name,
                "level": wild_pkmn.level,
                "types": wild_pkmn.types,
                "actStats": wild_pkmn.actStats
            })
            
            battle_turns = 0
            current_battle_turns = []
            
            while player_pkmn.able_to_fight and wild_pkmn.able_to_fight:
                battle_turns += 1

                # Player's Turn
                attacker = player_pkmn
                defender = wild_pkmn
                attacker_hp_before = attacker.curr_HP
                defender_hp_before = defender.curr_HP
                
                success, result, move_used = attacker.useRandomMove(defender, self.type_effectiveness_list, ignore_pp=True)

                damage_done = max(defender_hp_before - defender.curr_HP,0)

                current_battle_turns.append({
                    "turn": battle_turns,
                    "attacker": attacker.nickname,
                    "defender": defender.nickname,
                    "attacker_hp_before": attacker_hp_before,
                    "move": move_used["name"] if move_used else "unknown",
                    "damage": damage_done,
                    "defender_hp_after": defender.curr_HP
                })

                if not wild_pkmn.able_to_fight:
                    break

                # Opponent's Turn
                attacker = wild_pkmn
                defender = player_pkmn
                attacker_hp_before = attacker.curr_HP
                defender_hp_before = defender.curr_HP

                # if wild_pkmn.able_to_fight:
                #     wild_pkmn.useRandomMove(player_pkmn, self.type_effectiveness_list, ignore_pp=True)

                success, result, move_used = attacker.useRandomMove(defender, self.type_effectiveness_list, ignore_pp=True)
                damage_done = max(defender_hp_before - defender.curr_HP,0)

                current_battle_turns.append({
                    "turn": battle_turns,
                    "attacker": attacker.nickname,
                    "defender": defender.nickname,
                    "attacker_hp_before": attacker_hp_before,
                    "move": move_used["name"] if move_used else "unknown",
                    "damage": damage_done,
                    "defender_hp_after": defender.curr_HP
                })

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

            statistics["turns_details"].append(current_battle_turns)

            player_pkmn.heal()

            # To remove the random pkmn to the possible encounterable pokemon from the next steps
            wild_trainer.remove_pokemon(wild_pkmn.nickname)
        
        return statistics