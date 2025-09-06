import game_engine

def main():
    
    # Initialize FSM
    game_engine.game_engine_SM.initialize()
    
    # ENGINE
    exit = False
    while not exit:
        game_engine.game_engine_SM.eval_current()
        
        target = None
        if game_engine.game_engine_SM.state not in game_engine.game_engine_SM.final_states:
            target = game_engine.game_engine_SM.update()
            
        if not target:
            # Exit from simulation
            exit = True
        else:
            game_engine.game_engine_SM.do_transition(target)
    

if __name__ == "__main__":
    main()