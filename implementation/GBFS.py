from generic_search_algorithm import GenericSearchAlgorithm

class GBFSAlgorithm(GenericSearchAlgorithm):
  '''
  The GBFSAlgorithm class
  '''

  def __init__(self, puzzle_string, heuristic): # TESTED
    """
    The GBFSAlgorithm Constructor
    """
    super().__init__(puzzle_string, False, True, False, heuristic)

  # Implemented abstract method from parent class
  def get_node_cost(self, node): # TESTED
    """
    Method to get the cost of a Node
    """
    return node.value_h

