from abc import ABC, abstractmethod
from game_state import GameState
from node import Node
import time
import csv
import os

class GenericSearchAlgorithm(ABC):
  '''
  The GenericSearchAlgorithm class
  '''
  
  def __init__(self, puzzle_string, use_g, use_h, use_f, heuristic = None): # TESTED
    """
    The SearchAlgorithm Constructor
    """
    initial_gamestate = GameState.generate_initial_gamestate(puzzle_string)
    self.initial_node = Node.generate_initial_node(initial_gamestate, use_g, use_h, use_f, heuristic) # The initial node
    self.initial_board_configuration = puzzle_string  # The initial string passed
    self.open_list = [self.initial_node]              # The list that contains all open nodes (nodes to be visited/expanded)
    self.closed_list = []                             # The list that contains all closed nodes (nodes that were visited/expanded)
    self.search_path = []                             # The search path of the solution (the list of nodes that have been searched)
    self.solution_path = []                           # The solution path of the algorithm
    self.performance_time_seconds = 0                 # The amount of time it took to run the search_for_solution method (in seconds)
  
  def create_solution_and_search_files(self, subfolder, algorithm_acronym, heuristic_number, puzzle_number): # heuristic_number == None if no heuristic used
    """
    Method to write the algorithm solution and search output to a file
    """
    self.create_solution_file(subfolder, algorithm_acronym, heuristic_number, puzzle_number)
    self.create_search_file(subfolder, algorithm_acronym, heuristic_number, puzzle_number)

  def create_solution_file(self, subfolder, algorithm_acronym, heuristic_number, puzzle_number): # heuristic_number == None if no heuristic used
    """
    Method to write the algorithm solution output to a file
    """
    if (heuristic_number is None):
      output_file_name = algorithm_acronym + "-sol-" + str(puzzle_number) + ".txt"
    else:
      output_file_name = algorithm_acronym + "-" + heuristic_number + "-sol-" + str(puzzle_number) + ".txt"
    output_file_path =  os.path.join(os.getcwd(), "implementation", "output_files", subfolder, output_file_name)
    with open(output_file_path, "w") as f:
      f.write("Initial board configuration: " + self.initial_board_configuration + "\n\n")
      f.write(self.initial_node.game_state.get_grid_string_2d() + "\n\n")
      f.write(self.initial_node.game_state.get_fuel_amounts_string() + "\n\n")
      if (len(self.solution_path) > 1):
        f.write("Runtime: " + str(round(self.performance_time_seconds, 4)) + " seconds\n")
        f.write("Search path length: " + str(self.get_closed_list_size() + self.get_open_list_size()) + " states\n")
        solution_path_without_initial_node = self.solution_path[1:]
        f.write("Solution path length: " + str(len(solution_path_without_initial_node)) + " moves\n")
        solution_path_string = "Solution path: "
        for node in solution_path_without_initial_node:
          solution_path_string += node.game_state.get_change_string_no_format() + "; "
        solution_path_string = solution_path_string[:-2]
        f.write(solution_path_string + "\n\n")
        [f.write(node.game_state.get_data_string() + "\n") for node in solution_path_without_initial_node]
        f.write("\n")
        f.write(self.solution_path[-1].game_state.get_grid_string_2d() + "\n")
      elif (len(self.solution_path) == 1):
        f.write("Already the solution" + "\n")
      else:
        f.write("No solution" + "\n")
  
  def create_search_file(self, subfolder, algorithm_acronym, heuristic_number, puzzle_number): # heuristic_number == None if no heuristic used
    """
    Method to write the algorithm search output to a file
    """
    if (heuristic_number is None):
      output_file_name = algorithm_acronym + "-search-" + str(puzzle_number) + ".txt"
    else:
      output_file_name = algorithm_acronym + "-" + heuristic_number + "-search-" + str(puzzle_number) + ".txt"
    output_file_path = os.path.join(os.getcwd(), "implementation", "output_files", subfolder, output_file_name)
    with open(output_file_path, "w") as f:
      [f.write(self.get_search_file_string(node) + "\n") for node in self.search_path]

  def add_to_csv_file(self, subfolder, output_csv_name, algorithm_name, heuristic_number_with_h, puzzle_number):
    """
    Method to append a row to a csv file
    """
    output_file_path =  os.path.join(os.getcwd(), "implementation", "output_files", subfolder, output_csv_name)
    with open(output_file_path, 'a', newline='') as csv_file: 
      csv_writer = csv.writer(csv_file)

      # if the file is empty, add the header
      if os.stat(output_file_path).st_size == 0:
        csv_writer.writerow([
          "Puzzle Number",
          "Algorithm",
          "Heuristic",
          "Length of the Solution",
          "Length of the Search Path",
          "Execution Time (in seconds)"
        ])

      # Append the data to a row
      csv_writer.writerow([
        puzzle_number,
        algorithm_name,
        heuristic_number_with_h,
        len(self.solution_path) - 1, # -1 represents no solution, 0 represents initial puzzle was already in the solution state
        len(self.search_path),
        round(self.performance_time_seconds, 4)
      ])

  def get_closed_list_size(self): # TESTED
    """
    Method to get the length of the closed list
    """
    return len(self.closed_list)
  
  def get_open_list_size(self): # TESTED
    """
    Method to get the length of the open list
    """
    return len(self.open_list)

  def print_current_state(self): # TESTED
    """
    Testing method to print the current state of the algorithm (open and closed lists)
    """
    print("Step", "- Open List: [")
    [print("\t", self.get_search_file_string(node)) for node in self.open_list]
    print("]")
    print("Step", "- Closed List: [")
    [print("\t", self.get_search_file_string(node)) for node in self.closed_list]
    print("]")
  
  def get_search_file_string(self, node): # TESTED
    """
    Method to print the current search state of the algorithm (f(n), g(n), h(n), grid_string)
    """
    return '%4s %4s %4s %39s' % (
        node.value_f,
        node.value_g,
        node.value_h,
        node.game_state.grid_string)

  def search_for_solution(self): # TESTED
    """
    Method to find the solution of the initial Node/GameState
    """
    start_time = time.time()
    #self.print_current_state() # for testing
    while (not self.is_open_list_empty()):
      popped_node = self.pop_first_node_from_open_list()
      if (self.is_node_goal_state(popped_node)):
        self.add_node_to_closed_list(popped_node)
        self.set_solution_path(popped_node)
        break
      else:
        self.add_node_to_closed_list(popped_node)
        self.add_successors_to_open_list(popped_node)
      #self.print_current_state() # for testing
    end_time = time.time()
    self.performance_time_seconds = end_time - start_time
    self.set_solution_path(None) # No solution

  @abstractmethod # TO BE OVERRIDDEN IN CHILD CLASS
  def get_node_cost(self, node): # TESTED
    """
    Method to get the cost of a Node
    """
    pass

  # MIGHT HAVE TO BE OVERRIDDEN IN CHILD CLASS (depending on algorithm)
  def add_successors_to_open_list_extra_steps(self, successor_node, same_node_from_closed_list, same_node_from_open_list): # TESTED
    """
    Helper method to apply extra steps to the add_successors_to_open_list method, depending on the algorithm used
    """
    pass

  def add_successors_to_open_list(self, node): # TESTED
    """
    Method to add successor Nodes to the open list (and remove from same from closed/open list - depending on algorithm used)
    """
    for successor_node in node.generate_successor_nodes():
      same_node_from_closed_list = self.get_new_node_from_closed_list(successor_node)
      same_node_from_open_list = self.get_new_node_from_open_list(successor_node)
      if (same_node_from_closed_list == None and same_node_from_open_list == None):
        self.add_node_to_open_list_sorted(successor_node)
      else:
        self.add_successors_to_open_list_extra_steps(successor_node, same_node_from_closed_list, same_node_from_open_list)
  
  # --------------
  # Helper Methods
  # --------------

  # A
  def is_open_list_empty(self): # TESTED
    """
    Method to check if the open list is empty
    """
    return not bool(self.open_list)

  # B
  def pop_first_node_from_open_list(self): # TESTED
    """
    Method to pop (remove and return) the first node from the ordered open list
    """
    return self.open_list.pop(0)

  # C-1
  def is_node_goal_state(self, node): # TESTED
    """
    Method to check if the given node is a goal state
    """
    return node.game_state.get_change()["is_solution_state"]
  
  # C-2
  def set_solution_path(self, node): # TESTED
    """
    Method to get the solution path as a list of ordered nodes (the first being the initial game state)
    """
    if (node is not None):
      self.solution_path.append(node)
      current_node = node.parent_node
      while (current_node is not None):
        self.solution_path.insert(0, current_node)
        current_node = current_node.parent_node
  
  # D
  def add_node_to_closed_list(self, node): # TESTED
    """
    Method to add a node to the closed list
    """
    self.closed_list.insert(0, node)
    self.search_path.append(node)

  # E-1-i
  def get_new_node_from_closed_list(self, new_node): # TESTED
    """
    Method to get the same node from the closed list (with some different attributes - different object)
    """
    for node in self.closed_list:
      if node.game_state.grid_string == new_node.game_state.grid_string:
        return node
    return None

  # E-1-ii
  def get_new_node_from_open_list(self, new_node): # TESTED
    """
    Method to get the same node from the open list (with some different attributes - different object)
    """
    for node in self.open_list:
      if node.game_state.grid_string == new_node.game_state.grid_string:
        return node
    return None
  
  # E-2-i
  def remove_node_from_closed_list(self, node): # TESTED
    """
    Method to remove a node from the closed list
    """
    self.closed_list.remove(node)

  # E-2-ii
  def remove_node_from_open_list(self, node): # TESTED
    """
    Method to remove a node from the open list
    """
    self.open_list.remove(node)

  # E-3-i
  def add_node_to_open_list_sorted(self, node): # TESTED
    """
    Method to add a node to the open list, and then sort the list
    """
    self.open_list.append(node)
    self.sort_open_list()
  
  # E-3-ii
  def sort_open_list(self): # TESTED
    """
    Method to sort the open list
    """
    self.open_list.sort(key = lambda node: self.get_node_cost(node))
