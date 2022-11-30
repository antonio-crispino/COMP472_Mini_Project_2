from abc import ABC, abstractmethod
from game_state import GameState
from node import Node

class GenericSearchAlgorithm(ABC):
  '''
  The SearchAlgorithm class
  '''
  
  def __init__(self, puzzle_string, use_g, use_h, use_f, heuristic = None):
    """
    The SearchAlgorithm Constructor
    """
    initial_gamestate = GameState.generate_initial_gamestate(puzzle_string)
    initial_node = Node.generate_initial_node(initial_gamestate, use_g, use_h, use_f, heuristic)
    self.open_list = [initial_node]   # The list that contains all open nodes (nodes to be visited/expanded)
    self.closed_list = []             # The list that contains all closed nodes (nodes that were visited/expanded)

  # ----------------
  # Abstract Methods
  # ----------------

  @abstractmethod
  def search_for_solution(self): # TO BE OVERRIDDEN IN CHILD CLASS (Might not have to be) !!!
    """
    Method to find the solution of the initial Node/GameState
    """
    pass
  
  @abstractmethod
  def get_node_cost(self): # TO BE OVERRIDDEN IN CHILD CLASS
    """
    Method to get the cost of a Node
    """
    pass

  @abstractmethod
  def add_successors_to_open_list(self, node): # TO BE OVERRIDDEN IN CHILD CLASS
    """
    Method to add successor Nodes to the open list (and remove from closed list - depending on algorithm used)
    """
    pass
  
  # --------------
  # Helper Methods (Remove if methods are not used in search_for_solution method) !!!
  # --------------

  # A
  def is_open_list_empty(self):
    """
    Method to check if the open list is empty
    """
    return bool(self.open_list)

  # B
  def pop_first_node_from_open_list(self):
    """
    Method to pop (remove and return) the first node from the ordered open list
    """
    return self.open_list.pop(0)

  # C-1
  def is_node_goal_state(self, node):
    """
    Method to check if the given node is a goal state
    """
    return node.game_state.change["is_solution_state"]
  
  # C-2
  def get_solution_path(self, node):
    """
    Method to get the solution path as a list of ordered nodes (the first being the initial game state)
    """
    ordered_solution_nodes = [node]
    current_node = node
    while (current_node.parent_node != None):
      current_node = node.parent_node
      ordered_solution_nodes.insert(0, current_node)
    return ordered_solution_nodes
  
  # D
  def add_node_to_closed_list(self, node):
    """
    Method to add a node to the closed list
    """
    self.closed_list.insert(0, node)

  # E-1-i
  def get_new_node_from_closed_list(self, new_node):
    """
    Method to get the same node from the closed list (with some different attributes - different object)
    """
    for node in self.closed_list:
      if node.game_state.grid_string == new_node.game_state.grid_string:
        return node
    return None

  # E-1-ii
  def get_new_node_from_open_list(self, new_node):
    """
    Method to get the same node from the open list (with some different attributes - different object)
    """
    for node in self.open_list:
      if node.game_state.grid_string == new_node.game_state.grid_string:
        return node
    return None
  
  # E-2-i
  def remove_node_from_closed_list(self, node):
    """
    Method to remove a node from the closed list
    """
    self.closed_list.remove(node)

  # E-2-ii
  def remove_node_from_open_list(self, node):
    """
    Method to remove a node from the open list
    """
    self.open_list.remove(node)

  # E-3-i
  def add_node_to_open_list_sorted(self, node):
    """
    Method to add a node to the open list, and then sort the list
    """
    self.open_list.append(node)
    self.sort_open_list()
  
  # E-3-ii
  def sort_open_list(self):
    """
    Method to sort the open list
    """
    self.open_list.sort(key = lambda node: self.get_node_cost(node))
