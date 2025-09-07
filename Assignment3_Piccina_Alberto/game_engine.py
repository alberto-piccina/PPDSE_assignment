import FiniteStateMachine as FSM
import utils
import pokemon_trainer


# Adding pkmn_list and moves_list from .json's files
pkmn_list = utils.load_pokemons("pokemons.json")
moves_list = utils.load_filtered_moves("moves.json")
type_effectiveness_list = utils.load_from_file("type_effectiveness.json")


class StartGameState(FSM.State):
    def __init__(self, name="Start Game"):
        self.name = name

    def run(self, *args, **kargs):
        # List of Starters Pokemon
        starter_name_list = ["Bulbasaur", "Charmander", "Squirtle"]
        wild_starter_name_list = ["Caterpie", "Pidgey", "Rattata"]
        
        # Setup the Wild Pokemons
        for pkmn in wild_starter_name_list:
            wild.add_pokemon(pkmn_list, moves_list, pkmn, f"Wild {pkmn}")
        
        # Start Simulator and creation of the Trainer
        print("\n\nWELCOME TO THE 1st GEN POKEMON SIMULATOR!")
        print("Now, it is time to create your trainer:\n")
        trainer_name = input("What is your name? ")
        trainer.name = trainer_name
        print(f"Awesome! So your name is {trainer.name}.\n")
        
        # Choose of the starter Pokemon
        print("As a new trainer, you do not have any Pokemon in your team yet.")
        print("Choose your starter Pokemon between: ")
        for i, option in enumerate(starter_name_list):
            print("     ", i+1, ":", option)
        choice = int(input("Your choice: "))-1
        starter = starter_name_list[choice]
        nickname = input(f"Do you want to assign a nickname to {starter}? (Left blank if you do not want to assign a nickname) ")
        trainer.add_pokemon(pkmn_list, moves_list, starter, nickname)

        trainer.check_team()
        
        trainer.actual_pokemon = trainer.pokemon_list.get(nickname if nickname != "" else starter)
        
        # Adding 10 Potions and 10 Pokeballs to the Trainer's bag
        trainer.add_item("Potion", 10)
        trainer.add_item("Pokeball", 10)
        trainer.check_bag()
        
        print("\nNow, your trip begins! Good luck!\n\n")

    def update(self, choices, *args, **kargs):
        return story_state
        
    
class StoryState(FSM.State):
    def __init__(self, name="Story"):
        self.name = name

    def run(self, *args, **kargs):
        print("You are in Story mode.")

    def update(self, choices, *args, **kargs):
        print("Here is what you can do:")
        transitions = game_engine_SM.possible_transitions()
        for transition in transitions:
            if transition != story_state:
                print(f" - {transition.name}")
                
        next = input("What do you want to do? ")
        if next == "Exit":
            return exit_state
        elif next == "Pokemon Center":
            return pokemon_center_state
        elif next == "Pokemon Store":
            return pokemon_store_state
        elif next == "Explore":
            return explore_state
        else:
            print("Ops! It seems like you mistyped something.")
            return story_state
    
    
class PokemonCenterState(FSM.State):
    def __init__(self, name="Pokemon Center"):
        self.name = name

    def run(self, *args, **kargs):
        print("\n| Welcome to the Pokemon Center!", "| I'll take your Pokemon for a few seconds.", sep="\n")
        print("|", "-"*50, "|", sep="\n")
        
        for pkmn in trainer.pokemon_list:
            trainer.pokemon_list[pkmn].curr_HP = trainer.pokemon_list[pkmn].baseStats["hp"]
            trainer.pokemon_list[pkmn].able_to_fight = True
            print(f"| {trainer.pokemon_list[pkmn].nickname} ({trainer.pokemon_list[pkmn].name}) is healed up! ({trainer.pokemon_list[pkmn].curr_HP}/{trainer.pokemon_list[pkmn].baseStats['hp']} HP)")
            for move in trainer.pokemon_list[pkmn].moves:
                trainer.pokemon_list[pkmn].moves[move]["pp"] = trainer.pokemon_list[pkmn].moves[move]["max_pp"]
                print("|", " "*4, f"The PPs of {trainer.pokemon_list[pkmn].nickname}'s {move} are fully restored! ({trainer.pokemon_list[pkmn].moves[move]['pp']}/{trainer.pokemon_list[pkmn].moves[move]['max_pp']} PP)")
                
        print("|", "-"*50, "|", sep="\n")
            
        print("| Your Pokemons are all healed up!", "| We hope to see you again!\n", sep="\n")

    def update(self, choices, *args, **kargs):
        return story_state
    
    
class PokemonStoreState(FSM.State):
    def __init__(self, name="Pokemon Store"):
        self.name = name

    def run(self, *args, **kargs):
        print("\n| Welcome to the Pokemon Store!", "| I'll stock you up with plenty of Pokeballs and Potions!", sep="\n")
        print("|", "-"*50, "|", sep="\n")
        
        for item in trainer.items:
            if item == "Potion" and trainer.items.count(item) < 10:
                residual = trainer.items.count(item)
                to_fill = 10 - residual
                trainer.add_item(item, to_fill)
                print(f"| {trainer.name} received {to_fill} Potions.", "---> Current Number of Potions:", trainer.items.count(item))
            if item == "Pokeball" and trainer.items.count(item) < 10:
                residual = trainer.items.count(item)
                to_fill = 10 - residual
                trainer.add_item(item, to_fill)
                print(f"| {trainer.name} received {to_fill} Pokeballs.", "---> Current Number of Pokeballs:", trainer.items.count(item))
                
        print("|", "-"*50, "|", sep="\n")
        print("| Thank you! Please come again if you need more Potions and Pokeballs!\n")

    def update(self, choices, *args, **kargs):
        return story_state
    
    
class ExploreState(FSM.State):
    def __init__(self, name="Explore"):
        self.name = name
        self.prob_of_fight = 0.8
        self.move_to_battle = False

    def run(self, *args, **kargs):
        print("\n| New Pokemons and new battles -- It's time to explore!", "| Step into the tall grass and see what you can find!", sep="\n")
        print("|", "-"*50, "|", sep="\n")
        
        print(f"| Probability of encounter a wild Pokemon: {self.prob_of_fight*100}%")
        probability = pokemon_trainer.pokemon.random.random()
        print(f"| Actual random number: {probability*100}%")
        
        if probability < self.prob_of_fight:
            self.move_to_battle = True
            # print("| A wild Pokemon appeared!")
        else:
            print("| Nothing happened.")
            print("|", "-"*50, "|\n", sep="\n")

    def update(self, choices, *args, **kargs):
        if self.move_to_battle:
            self.move_to_battle = False
            return battle_state
        else:
            return story_state
    
    
class BattleState(FSM.State):
    def __init__(self, name="Battle"):
        self.name = name
        self.prob_of_run_away = 1
        self.outcome = False # True if the trainer wins/catch/run away the battle, False otherwise

    def run(self, *args, **kargs):
        rdn_pkmn = pokemon_trainer.pokemon.random.choice(list(wild.pokemon_list.values()))
        print(f"| A {rdn_pkmn.nickname} appeared!")
        print("|", "-"*50, "|", sep="\n")
        print(f"| Your actual Pokemon: {trainer.actual_pokemon.nickname} ({trainer.actual_pokemon.name})")
        
        list_of_actions = ["Attack", "Change Pokemon", "Use Item", "Run Away"]
        
        __ongoing = True
        while __ongoing:
            if not trainer.actual_pokemon.able_to_fight:
                    print(f"| {trainer.actual_pokemon.nickname} is not able to fight anymore.\n")
                    if all(not pokemon.able_to_fight for pokemon in trainer.pokemon_list.values()):
                        print("| You don't have any Pokemon able to fight anymore.\n")
                        rdn_pkmn.curr_HP = rdn_pkmn.baseStats["hp"]
                        __ongoing = False
                        self.outcome = False
                    else:
                        print("| Which Pokemon do you want to use? ")
                        trainer.check_team()
                        next_pokemon = input("| Your choice: ")
                        trainer.actual_pokemon = trainer.pokemon_list.get(next_pokemon)
                        
            print("\n| It's your turn!", "| What do you want to do?", sep="\n")
            for action in list_of_actions:
                print(" - ", action)
            choice = input("--> ")
            
            if choice == "Attack":
                print("| Here is the move's list of your Pokemon:")
                for i,j in trainer.actual_pokemon.moves.items():
                    print("     -->", i, ":", j["pp"], "PP")
                move_to_use = input(f'| What {trainer.actual_pokemon.nickname} ({trainer.actual_pokemon.name}) should do? ')
                
                trainer.actual_pokemon.useMove(trainer.actual_pokemon.moves[move_to_use], rdn_pkmn, type_effectiveness_list)
                if not rdn_pkmn.able_to_fight:
                    print(f"| {rdn_pkmn.nickname} is not able to fight anymore.\n")
                    rdn_pkmn.curr_HP = rdn_pkmn.baseStats["hp"]
                    rdn_pkmn.able_to_fight = True
                    __ongoing = False
                    self.outcome = True
                else:
                    rdn_pkmn.useRandomMove(trainer.actual_pokemon, type_effectiveness_list)
                
            elif choice == "Change Pokemon":
                print("\n| Which Pokemon do you want to use?")
                for pokemon in trainer.pokemon_list:
                    print(" - ", trainer.pokemon_list[pokemon].nickname)
                new_pkmn = input("| Your choice: ")
                trainer.actual_pokemon = trainer.pokemon_list[new_pkmn]
                print(f"| {trainer.actual_pokemon.nickname} is now your actual Pokemon.")
                rdn_pkmn.useRandomMove(trainer.actual_pokemon)
                
            elif choice == "Use Item":
                print("| Which item do you want to use?")
                trainer.check_bag()
                item = input("| Your choice: ")
                if item == "Potion":
                    trainer.use_item(item)
                    trainer.actual_pokemon.curr_HP = min(trainer.actual_pokemon.curr_HP + 20, trainer.actual_pokemon.baseStats["hp"])
                    rdn_pkmn.useRandomMove(trainer.actual_pokemon)
                elif item == "Pokeball":
                    trainer.use_item(item)
                    catchProbability = 1- (rdn_pkmn.curr_HP / rdn_pkmn.baseStats["hp"])
                    probability = pokemon_trainer.pokemon.random.random()
                    if probability < catchProbability:
                        print(f"| You caught {rdn_pkmn.nickname}!")
                        new_pokemon = pokemon_trainer.copy.deepcopy(rdn_pkmn)
                        nickname = input(f"| Do you want to assign a nickname to {new_pokemon.name}? (Left blank if you do not want to assign a nickname) ")
                        print("\n")
                        new_pokemon.nickname = nickname if nickname != "" else new_pokemon.name
                        trainer.pokemon_list[new_pokemon.nickname] = new_pokemon
                        rdn_pkmn.curr_HP = rdn_pkmn.baseStats["hp"]
                        __ongoing = False
                        self.outcome = True
                    else:
                        print("| The caught didn't work!")
                        rdn_pkmn.useRandomMove(trainer.actual_pokemon)
                else:
                    print(f"| {item} not found!", "Please choose another item.")
                    rdn_pkmn.useRandomMove(trainer.actual_pokemon)
                
            elif choice == "Run Away":
                probability = pokemon_trainer.pokemon.random.random()
                if probability < self.prob_of_run_away:
                    print("| You successfully ran away!\n")
                    rdn_pkmn.curr_HP = rdn_pkmn.baseStats["hp"]
                    __ongoing = False
                    self.outcome = True
                else:
                    print("| You couldn't run away!\n")
                    rdn_pkmn.useRandomMove(trainer.actual_pokemon)
                
            else:
                print("Ops! It seems like you mistyped something.")
        
    def update(self, choices, *args, **kargs):
        if self.outcome == True:
            return story_state
        else:
            return pokemon_center_state
    
    
class ExitState(FSM.State):
    def __init__(self, name="Exit"):
        self.name = name

    def run(self, *args, **kargs):
        print("\nEXIT FROM SIMULATION")

    def update(self, choices, *args, **kargs):
        pass
    


game_engine_SM = FSM.FiniteStateMachine()
trainer = pokemon_trainer.Trainer()

# Create the Wild Pokemon Team
wild = pokemon_trainer.Trainer("Wild")
    
# Create instances of states
start_state = StartGameState()
story_state = StoryState()
pokemon_center_state = PokemonCenterState()
pokemon_store_state = PokemonStoreState()
explore_state = ExploreState()
battle_state = BattleState()
exit_state = ExitState()

# Add states to the FSM
game_engine_SM.add_state(start_state)
game_engine_SM.add_state(story_state)
game_engine_SM.add_state(pokemon_center_state)
game_engine_SM.add_state(pokemon_store_state)
game_engine_SM.add_state(explore_state)
game_engine_SM.add_state(battle_state)
game_engine_SM.add_state(exit_state)

# Define transitions
game_engine_SM.add_transition(start_state, story_state)
game_engine_SM.add_transition(story_state, exit_state)
game_engine_SM.add_transition(story_state, pokemon_center_state)
game_engine_SM.add_transition(pokemon_center_state, story_state)
game_engine_SM.add_transition(story_state, pokemon_store_state)
game_engine_SM.add_transition(pokemon_store_state, story_state)
game_engine_SM.add_transition(story_state, explore_state)
game_engine_SM.add_transition(explore_state, story_state)
game_engine_SM.add_transition(explore_state, battle_state)
game_engine_SM.add_transition(battle_state, pokemon_center_state)
game_engine_SM.add_transition(battle_state, story_state)

# Transition in case of mistyping
game_engine_SM.add_transition(story_state, story_state)

# Set the start state and final states
game_engine_SM.set_start_state(start_state)
game_engine_SM.set_final_states([exit_state])