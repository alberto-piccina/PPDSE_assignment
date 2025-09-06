import pokemon_trainer
import utils


# Initialization testing

pkmn_list = utils.load_from_file("pokemon_data.json")
moves_list = utils.load_from_file("moves.json")
    
trainer1 = pokemon_trainer.Trainer("Alberto")
trainer2 = pokemon_trainer.Trainer("Mattia")

# print("\nTrainer 1 is called", trainer1.name, ", he has", len(trainer1.pokemon_list), "Pokemon with him and", len(trainer1.items), "items in his bag.")
# print("Trainer 2 is called", trainer2.name, ", he has", len(trainer2.pokemon_list), "Pokemon with him and", len(trainer2.items), "items in his bag.\n")


# Function "add_item" testing
# trainer1.add_item("pozione")
# trainer1.add_item("superpozione")
# trainer1.add_item("antidoto")

# trainer2.add_item("pokeball")
# trainer2.add_item("lastrafuoco")


# Function "check_bag" testing
# trainer1.check_bag()
# trainer2.check_bag()


# Function "use_item" testing
# trainer1.use_item("superpozione")
# trainer1.use_item("baccafragola")
# trainer1.add_item("pozione")
# trainer1.add_item("pozione")
# trainer1.add_item("pozione")
# trainer1.add_item("pozione")
# trainer1.check_bag()
# trainer2.check_bag()



# Functions about team managing testing

# TEST1
# trainer1.add_pokemon("Charmender", pkmn_list, moves_list)
# trainer1.check_team()
# trainer1.remove_pokemon("Charmender")
# trainer1.check_team()


# TEST2
# trainer1.add_pokemon("Squirtle", pkmn_list, moves_list)
# trainer1.add_pokemon("Charmender", pkmn_list, moves_list)
# trainer1.check_team()
# trainer1.remove_pokemon("Squirtle")
# trainer1.check_team()
# trainer1.remove_pokemon("Charmender")
# trainer1.check_team()


# TEST3
# trainer1.add_pokemon("Bulbasaur", pkmn_list, moves_list)
# trainer1.add_pokemon("Squirtle", pkmn_list, moves_list)

# trainer2.add_pokemon("Bulbasaur", pkmn_list, moves_list)
# trainer2.add_pokemon("Charmender", pkmn_list, moves_list)

# trainer1.check_team()
# trainer2.check_team()

# trainer1.remove_pokemon("Bulbasaur")
# trainer1.check_team()
# trainer2.check_team()

# trainer1.remove_pokemon("Bulbasaur")
# trainer1.check_team()
# trainer2.check_team()

# trainer1.pokemon_list.clear()
# trainer2.pokemon_list.clear()
# trainer1.check_team()
# trainer2.check_team()


# TEST4
# trainer1.add_pokemon("Bulbasaur", pkmn_list, moves_list)
# trainer2.add_pokemon("Bulbasaur", pkmn_list, moves_list)

# trainer1.pokemon_list["Bulbasaur"].useMove(trainer1.pokemon_list["Bulbasaur"].moves["Tackle"], trainer2.pokemon_list["Bulbasaur"])
# trainer1.pokemon_list["Bulbasaur"].useMove(trainer1.pokemon_list["Bulbasaur"].moves["Razor Leaf"], trainer2.pokemon_list["Bulbasaur"])
# trainer1.pokemon_list["Bulbasaur"].useMove(trainer1.pokemon_list["Bulbasaur"].moves["Tackle"], trainer2.pokemon_list["Bulbasaur"])
# trainer2.pokemon_list["Bulbasaur"].useMove(trainer2.pokemon_list["Bulbasaur"].moves["Razor Leaf"], trainer1.pokemon_list["Bulbasaur"])
# trainer2.pokemon_list["Bulbasaur"].useMove(trainer2.pokemon_list["Bulbasaur"].moves["Razor Leaf"], trainer1.pokemon_list["Bulbasaur"])
# trainer1.check_team()
# trainer2.check_team()

# trainer1.pokemon_list.clear()
# trainer2.pokemon_list.clear()
# trainer1.check_team()
# trainer2.check_team()

# trainer1.add_pokemon("Bulbasaur", pkmn_list, moves_list)
# trainer2.add_pokemon("Bulbasaur", pkmn_list, moves_list)
# trainer1.check_team()
# trainer2.check_team()

# trainer1.pokemon_list.clear()
# trainer2.pokemon_list.clear()
# trainer1.check_team()
# trainer2.check_team()


# TEST5
trainer1.add_pokemon(pkmn_list, moves_list, "Bulbasaur", "Bulb1")
trainer1.add_pokemon(pkmn_list, moves_list, "Bulbasaur")
trainer1.add_pokemon(pkmn_list, moves_list, "Charmender", "Charm1")
trainer1.add_pokemon(pkmn_list, moves_list, "Squirtle")
trainer1.add_pokemon(pkmn_list, moves_list, "Charmender")
trainer1.add_pokemon(pkmn_list, moves_list, "Squirtle", "Squirtle1")
trainer2.add_pokemon(pkmn_list, moves_list, "Bulbasaur")
trainer1.add_pokemon(pkmn_list, moves_list, "Bulbasaur", "Bulb2")
trainer1.check_team()
trainer2.check_team()

trainer1.pokemon_list["Bulb1"].useMove(trainer1.pokemon_list["Bulb1"].moves["Tackle"], trainer2.pokemon_list["Bulbasaur"])
trainer1.pokemon_list["Bulbasaur"].useMove(trainer1.pokemon_list["Bulbasaur"].moves["Tackle"], trainer2.pokemon_list["Bulbasaur"])
trainer2.pokemon_list["Bulbasaur"].useMove(trainer2.pokemon_list["Bulbasaur"].moves["Tackle"], trainer1.pokemon_list["Bulbasaur"])
trainer1.pokemon_list["Bulb1"].useMove(trainer1.pokemon_list["Bulb1"].moves["Razor Leaf"], trainer2.pokemon_list["Bulbasaur"])
trainer1.pokemon_list["Bulb1"].useMove(trainer1.pokemon_list["Bulb1"].moves["Razor Leaf"], trainer2.pokemon_list["Bulbasaur"])
trainer1.check_team()
trainer2.check_team()