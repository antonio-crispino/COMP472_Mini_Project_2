from game import GameState

initial_gamestate = GameState.generate_initial_gamestate("RRB...C.B...C.AA........EEGGG....... C3 B4 H1 F2")
successor_gamestates = initial_gamestate.generate_successor_gamestates()

print(initial_gamestate.get_data_string(), "\tis_solution_state:", initial_gamestate.get_change()["is_solution_state"])
[print(succssor.get_data_string(), "\tis_solution_state:", succssor.get_change()["is_solution_state"]) for succssor in successor_gamestates]
