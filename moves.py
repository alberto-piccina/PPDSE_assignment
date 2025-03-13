class Move:
    def __init__(self, name, type, category, power, accuracy, pp):
        self.name = name
        self.type = type
        self.category = category
        self. power = power
        self.accuracy = accuracy
        self.pp = pp
        
        
tackle = Move(
    name = "Tackle",
    type = "normal",
    category = "physical",
    power = 35,
    accuracy = 0.95,
    pp = 35
)

razor_leaf = Move(
    name = "Razor Leaf",
    type = "grass",
    category = "physical",
    power = 55,
    accuracy = 0.95,
    pp = 25
)

ember = Move(
    name = "Ember",
    type = "fire",
    category = "special",
    power = 40,
    accuracy = 1.0,
    pp = 25
)

water_gun = Move(
    name = "Water Gun",
    type = "water",
    category = "special",
    power = 40,
    accuracy = 1.0,
    pp = 25
)