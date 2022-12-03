from generic_search_algorithm import GenericSearchAlgorithm

class UCSAlgorithm(GenericSearchAlgorithm):
  '''
  The UCSAlgorithm class (Uniform Cost Search)
  '''

  def __init__(self, puzzle_string, heuristic): # TESTED
    """
    The UCSAlgorithm Constructor
    """
    super().__init__(puzzle_string, True, False, False, heuristic)

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
    """
    if ((same_node_from_closed_list is not None) and (self.get_node_cost(successor_node) < self.get_node_cost(same_node_from_closed_list))):
      self.remove_node_from_closed_list(same_node_from_closed_list)
      self.add_node_to_open_list_sorted(successor_node)
    elif ((same_node_from_open_list is not None) and (self.get_node_cost(successor_node) < self.get_node_cost(same_node_from_open_list))):
      self.remove_node_from_open_list(same_node_from_open_list)
      self.add_node_to_open_list_sorted(successor_node)
