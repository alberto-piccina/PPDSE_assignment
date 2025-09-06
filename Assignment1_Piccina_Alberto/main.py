import pokemon_trainer
import utils

def main():
    
    # Adding pkmn_list and moves_list from .json's files
    pkmn_list = utils.load_from_file("pokemon_data.json")
    moves_list = utils.load_from_file("moves.json")
    
    # List of 3 starter's Pokemon
    starter_name_list = ["Bulbasaur", "Charmender", "Squirtle"]
    
    # Start Simulator and creation of the Trainer
    print("\n\nWELCOME TO THE 1st GEN POKEMON SIMULATOR!")
    print("Now, it is time to create your trainer:\n")
    trainer_name = input("What is your name? ")
    trainer = pokemon_trainer.Trainer(trainer_name)
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
    print("\n")
    
    # Adding a Wild Pokemon to simulate a fight
    wild = pokemon_trainer.Trainer("Wild")
    wild_pkmn = starter_name_list[choice+1] if choice<2 else starter_name_list[choice-1]
    wild.add_pokemon(pkmn_list, moves_list, wild_pkmn, f"Wild {wild_pkmn}")
    
    # Fight Simulation
    number_of_fights = 15
    print("\n\nIt's time to fight!")
    print(f"{wild.pokemon_list.get(f'Wild {wild_pkmn}').nickname} appeared!")
    
    for i in range(number_of_fights):
        if not wild.pokemon_list[f"Wild {wild_pkmn}"].able_to_fight:
            print(f"{wild.pokemon_list[f'Wild {wild_pkmn}'].nickname} is not able to fight anymore.")
            break
        elif not trainer.pokemon_list[nickname if nickname != "" else starter].able_to_fight:
            print(f"{trainer.pokemon_list[nickname if nickname != '' else starter].nickname} is not able to fight anymore.")
            break
        else:
            print("\nWhich move do you want to use?")
            for i,j in trainer.pokemon_list.get(nickname if nickname != "" else starter).moves.items():
                print("-->", i, ":", j["pp"], "PP")
            move_to_use = input(f'What {trainer.pokemon_list.get(nickname if nickname != "" else starter).nickname} should do? ')
            
            trainer.pokemon_list[nickname if nickname != "" else starter].useMove(trainer.pokemon_list[nickname if nickname != "" else starter].moves[move_to_use], wild.pokemon_list[f"Wild {wild_pkmn}"])
            
            wild.pokemon_list[f"Wild {wild_pkmn}"].useRandomMove(trainer.pokemon_list[nickname if nickname != "" else starter])
    
    print("End of the Simulation.")

if __name__ == "__main__":
    main()