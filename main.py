import pokemon_trainer as trainer
import pokemon as pkmn

bulbasaur = pkmn.Pokemon(
    name = "Bulbasaur",
    national_pokedex_number = 1,
    types = ["grass", "poison"],
    baseStats = {
        "hp": 45,
        "attack" : 49,
        "defense" : 49,
        "speed" : 45,
        "special" : 65},
    moves = [pkmn.moves.tackle, pkmn.moves.razor_leaf]
)

charmender = pkmn.Pokemon(
    name = "Charmender",
    national_pokedex_number = 4,
    types = ["fire"],
    baseStats = {
        "hp": 39,
        "attack" : 52,
        "defense" : 43,
        "speed" : 65,
        "special" : 50},
    moves = [pkmn.moves.tackle, pkmn.moves.ember, pkmn.moves.razor_leaf]
)

squirtle = pkmn.Pokemon(
    name = "Squirtle",
    national_pokedex_number = 7,
    types = ["water"],
    baseStats = {
        "hp": 44,
        "attack" : 48,
        "defense" : 65,
        "speed" : 43,
        "special" : 50},
    moves = [pkmn.moves.tackle, pkmn.moves.water_gun]
)

def main():
    
    starters = [bulbasaur, charmender, squirtle]
    
    print("\n \n Welcome to the 1st Gen Pokemon Simulator!\n")
    trainer_name = input("What's your name? ")
    print("\n \n Choose you favorite starter Pokemon between:")
    for i, opt in enumerate(starters):
        print(i+1, ":", opt.name)
    choice = int(input("What's your choice? ")) - 1
    print("\n")
    
    trainer1 = trainer.Trainer(
        name = trainer_name
    )
    
    trainer1.add_pokemon(starters[choice])
    trainer1.check_team()

if __name__=="__main__":
    main()