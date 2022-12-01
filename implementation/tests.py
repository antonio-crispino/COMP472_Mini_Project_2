from game_state import GameState
from node import Node
from heuristic import Heuristic
from a_star_algorithm import AStarAlgorithm

# TEST GAMESTATE
initial_gamestate = GameState.generate_initial_gamestate("BBBJCCH..J..HAAJKK...DDLEEI..L..I.GG") # RRB...C.B...C.AA........EEGGG....... C3 B4 H1 F2
successor_gamestates = initial_gamestate.generate_successor_gamestates()
# print(initial_gamestate.get_data_string(), "\tis_solution_state:", initial_gamestate.get_change()["is_solution_state"])
# [print(successor.get_data_string(), "\tis_solution_state:", successor.get_change()["is_solution_state"]) for successor in successor_gamestates]

# TEST NODE
initial_node = Node.generate_initial_node(initial_gamestate, True, False, False, None)
successor_nodes = initial_node.generate_successor_nodes()
# print(initial_node.game_state.get_data_string(), "\tis_solution_state:", initial_node.game_state.get_change()["is_solution_state"])
# [print(successor.game_state.get_data_string(), "\tis_solution_state:", successor.game_state.get_change()["is_solution_state"]) for successor in successor_nodes]

# TEST HEURISTIC
# print(initial_gamestate.get_grid())
# print(Heuristic.get_blocked_positions_list(initial_gamestate))
# print(Heuristic.h1_number_of_blocking_vehicles(initial_gamestate))
# print(Heuristic.h2_number_of_blocked_positions(initial_gamestate))
# print(Heuristic.h3_number_of_blocking_vehicles_multiplied_by_constant_5(initial_gamestate))
# print(Heuristic.h4_number_of_blocking_vehicles_multiplied_by_number_of_blocked_positions(initial_gamestate))

# TEST ASTARALGORITHM
input_string_1 = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL."
input_string_2 = "..I...BBI.K.GHAAKLGHDDKLG..JEEFF.J.."
input_string_3 = "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH..."
input_string_4 = "BBB..MCCDD.MAAKL.MJ.KLEEJ.GG..JHHHII J0 B4"
input_string_5 = "IJBBCCIJDDL.IJAAL.EEK.L...KFF..GGHH. F0 G6"
input_string_6 = "BB.G.HE..G.HEAAG.I..FCCIDDF..I..F..."

algo = AStarAlgorithm(input_string_2, Heuristic.h1_number_of_blocking_vehicles)
print(algo.open_list[0].game_state.get_grid())
result = algo.search_for_solution()
if not bool(result):
  print("No solution")
[print(node.game_state.get_data_string()) for node in result]
print(algo.get_closed_list_size())
print(algo.get_open_list_size())
print(algo.get_closed_list_size() + algo.get_open_list_size())
print(algo.number_of_steps)
