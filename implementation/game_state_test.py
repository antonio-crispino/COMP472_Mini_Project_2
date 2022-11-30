from game_state import GameState

initial_gamestate = GameState.generate_initial_gamestate("RRB...C.B...C.AA........EEGGG....... C3 B4 H1 F2")
successor_gamestates = initial_gamestate.generate_successor_gamestates()

print(initial_gamestate.get_data_string(), "\tis_solution_state:", initial_gamestate.get_change()["is_solution_state"])
[print(successor.get_data_string(), "\tis_solution_state:", successor.get_change()["is_solution_state"]) for successor in successor_gamestates]
