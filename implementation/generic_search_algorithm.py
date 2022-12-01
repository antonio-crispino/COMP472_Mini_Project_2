from abc import ABC, abstractmethod
from game_state import GameState
from node import Node

class GenericSearchAlgorithm(ABC):
  '''
  The GenericSearchAlgorithm class
  '''
  
  def __init__(self, puzzle_string, use_g, use_h, use_f, heuristic = None): # TESTED
    """
    The SearchAlgorithm Constructor
    """
    initial_gamestate = GameState.generate_initial_gamestate(puzzle_string)
    initial_node = Node.generate_initial_node(initial_gamestate, use_g, use_h, use_f, heuristic)
    self.open_list = [initial_node]   # The list that contains all open nodes (nodes to be visited/expanded)
    self.closed_list = []             # The list that contains all closed nodes (nodes that were visited/expanded)
    self.number_of_steps = 1          # The number of steps that have taken place in the algorithm
    
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
    print("Step", self.number_of_steps, "- Open List: [")
    [print("\t", self.get_search_file_string(node)) for node in self.open_list]
    print("]")
    print("Step", self.number_of_steps, "- Closed List: [")
    [print("\t", self.get_search_file_string(node)) for node in self.closed_list]
    print("]")
  
  def get_search_file_string(self, node): # TESTED
    """
    Method to print the current search state of the algorithm (g(n), h(n), f(n), grid_string)
    """
    return '%4s %4s %4s %39s' % (
        node.value_g,
        node.value_h,
        node.value_f,
        node.game_state.grid_string)

  def search_for_solution(self): # TESTED
    """
    Method to find the solution of the initial Node/GameState
    """
    #self.print_current_state() # for testing
    while (not self.is_open_list_empty()):
      popped_node = self.pop_first_node_from_open_list()
      if (self.is_node_goal_state(popped_node)):
        return self.get_solution_path(popped_node)
      else:
        self.add_node_to_closed_list(popped_node)
        self.add_successors_to_open_list(popped_node)
      self.number_of_steps += 1
      #self.print_current_state() # for testing
    return [] # No solution

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
  def get_solution_path(self, node): # TESTED
    """
    Method to get the solution path as a list of ordered nodes (the first being the initial game state)
    """
    ordered_solution_nodes = [node]
    current_node = node.parent_node
    while (current_node is not None):
      ordered_solution_nodes.insert(0, current_node)
      current_node = current_node.parent_node
    return ordered_solution_nodes
  
  # D
  def add_node_to_closed_list(self, node): # TESTED
    """
    Method to add a node to the closed list
    """
    self.closed_list.insert(0, node)

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
