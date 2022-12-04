from generic_search_algorithm import GenericSearchAlgorithm

class GBFS(GenericSearchAlgorithm):
  '''
  The GBFSAlgorithm class
  '''

  def __init__(self, puzzle_string, heuristic): # TESTED
    """
    The GBSFAlgorithm Constructor
    """
    super().__init__(puzzle_string, False, True, True, heuristic)

  # Implemented abstract method from parent class
  def get_node_cost(self, node): # TESTED
    """
    Method to get the cost of a Node
    """
    return node.value_h

