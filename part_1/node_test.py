from game import GameState
from node import Node

initial_gamestate = GameState.generate_initial_gamestate("RRB...C.B...C.AA........EEGGG....... C3 B4 H1 F2")
initial_node = Node.generate_initial_node(initial_gamestate, True, False, False, None)
successor_nodes = initial_node.generate_successor_nodes()

print(initial_node.game_state.get_data_string(), "\tis_solution_state:", initial_node.game_state.get_change()["is_solution_state"])
[print(successor.game_state.get_data_string(), "\tis_solution_state:", successor.game_state.get_change()["is_solution_state"]) for successor in successor_nodes]
