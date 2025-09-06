# PPDSE: Alberto Piccina -> Assignment No.1
The goal of this first assignment is to build the main elements composing the *Pokemon Game*.
To complete the assignment, the following features are implemented:
- **Main Classes**: Pokemon Trainer and Pokemon;
- **Combat Management**;
- **main()** function to test the previous requests.

## Project Description
The Classes ```pokemon``` and ```pokemon_trainer``` can be found ```pokemon.py``` and ```pokemon_trainer.py```, respectively.
In ```pokemon_data.json```, it is possible to add any Pokemon as a dictionary, specifying:
- name
- national_pokedex_number
- types
- baseStats
- moves
Similarly, in ```moves.json```, a move is defined as a dictionary with the following attributes:
- name
- type
- category
- power
- accuracy
- pp
The file ```class.testing.py``` contains an intensive testing of the methods included in each Class, and furthermore the ```main.py``` allows to test the functions by the user from the terminal.
In detail, this latter Python file allows to perform a full simulation of a fight against a wild Pokemon that attacks you with a random move from its moveset. The number of turns of the battle can be modified from the ```main.py``` file itself thanks to the variable ```number_of_fights```. The simulation ends when the counter of turns becomes zero or when one of the two Pokemon is not able to fight anymore.

## Add-ons
In the file ```utils.py```, the function *load_from_file(filename)* allows to load Pokemons and Moves from .json's files.
In *pokemon_trainer* Class, there are some methods to manage the items and the bag.
In order to avoid any misunderstandings in the case of multiple Pokemon with the same name in the Trainer's team, the attribute *nickname* is introduced and can be decided when adding a new Pokemon in the team. If no *nickname* is specified, the new Pokemon will have his name as nickname, but it is not possible to have multiple Pokemon with the same name.