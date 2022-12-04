from generic_search_algorithm import GenericSearchAlgorithm

class UCSAlgorithm(GenericSearchAlgorithm):
  '''
  The UCSAlgorithm class (Uniform Cost Search)
  '''

  def __init__(self, puzzle_string): # TESTED
    """
    The UCSAlgorithm Constructor
    """
    super().__init__(puzzle_string, True, False, False, heuristic=None)

  # Implemented abstract method from parent class
  def get_node_cost(self, node): # TESTED
    """
    Method to get the cost of a Node
    """
    return node.value_g
