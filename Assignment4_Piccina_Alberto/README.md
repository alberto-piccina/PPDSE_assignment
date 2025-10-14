# PPDSE: Alberto Piccina -> Assignment No.2
The goal of the second assignment is to build the *Game Engine*.
To complete the assignment, the following features are implemented:
- **Creation of the Character** (similar to Assignment No.1);
- **Manage the Story**: the player can choose what to do and where to go;
- **Manage a Full Battle** against a wild Pokemon (this feature was implemented in the previous assignment, but here it will be improved);
- **main()** function to test the previous requests.

## Project Description
In this assignment, the Finite State Machine Approach ```FiniteStateMachine.py``` is adopted to implement the Game Engine of the simulator.
In ```game_engine.py```, each State of the State Machine is reported and the *game_engine_SM* is set.

Wild Pokemons are considered as part of a trainer's team, called *wild*.

To visualize the connection between each State, use the method *draw()* of *FiniteStateMachine*, or take a look to the pdf's file of the assignment.

## Add-ons
In the file ```requirements.txt``` are reported the Python packages used for this project.
Create a Pyhton environment and install them before running the code.