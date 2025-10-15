import random
import pokemon_trainer
import pandas as pd
import utils

pokemons_df = utils.load_pokemons("pokemons.json")
print(pokemons_df.info)

moves_df = utils.load_filtered_moves("moves.json")
print(moves_df.info)

types_df = utils.load_type_effectiveness("type_effectiveness.json")
print(types_df.info)