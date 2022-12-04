from generic_search_algorithm import GenericSearchAlgorithm

class AStarAlgorithm(GenericSearchAlgorithm):
  '''
  The AStarAlgorithm class (Algorithm A⋆)
  '''

  def __init__(self, puzzle_string, heuristic): # TESTED
    """
    The AStarAlgorithm Constructor
    """
    super().__init__(puzzle_string, True, True, True, heuristic)

  # Implemented abstract method from parent class
  def get_node_cost(self, node): # TESTED
    """
    Method to get the cost of a Node
    """
    return node.value_f
  
  # Overridden method from parent class
  def add_successors_to_open_list_extra_steps(self, successor_node, same_node_from_closed_list, same_node_from_open_list): # TESTED
    """
    Helper method to apply extra steps to the add_successors_to_open_list method, depending on the algorithm used
    It is overridden here to make algorithm A become A*
    """
    if ((same_node_from_closed_list is not None) and (self.get_node_cost(successor_node) < self.get_node_cost(same_node_from_closed_list))):
      self.remove_node_from_closed_list(same_node_from_closed_list)
      self.add_node_to_open_list_sorted(successor_node)
    elif ((same_node_from_open_list is not None) and (self.get_node_cost(successor_node) < self.get_node_cost(same_node_from_open_list))):
      self.remove_node_from_open_list(same_node_from_open_list)
      self.add_node_to_open_list_sorted(successor_node)
