class Node:
  '''
  The Node class
  '''
  
  def __init__(self, parent_node, game_state, depth, use_g, use_h, use_f, heuristic): # TESTED
    """
    The Node Constructor
    """
    self.parent_node = parent_node                                # Node: The parent node of the current node (None if initial node)
    self.game_state = game_state                                  # GameState: The GameState object of the current node
    self.action = game_state.get_change()["direction_moved"]      # String: The action (direction) performed to arrive at the current node
    self.depth = depth                                            # Number: The depth of the current node with respect to a tree representation
    self.heuristic = heuristic                                    # Function or None: The heuristic function (if no heuristic, then equals None)
    self.use_g = use_g                                            # Boolean: Whether or not to use the g(n) value
    self.use_h = use_h                                            # Boolean: Whether or not to use the h(n) value
    self.use_f = use_f                                            # Boolean: Whether or not to use the f(n) value
    self.value_g = depth if use_g else 0                          # Number: g(n) - The actual cost of the path from start to node n. (path cost equal depth in this case)
    self.value_h = heuristic(game_state) if use_h else 0          # Number: h(n) - The estimate of the cost to reach goal from node n.
    self.value_f = (self.value_g + self.value_h) if use_f else 0  # Number: f(n) - The estimate of the total cost along the path through n.

  @classmethod
  def generate_initial_node(cls, game_state, use_g, use_h, use_f, heuristic = None): # TESTED
    """
    Class method that creates the first Node
    """
    return Node(None, game_state, 0, use_g, use_h, use_f, heuristic)

  def generate_successor_nodes(self): # TESTED
    """
    Method that creates the child Nodes of the Node
    """
    successor_gamestates = self.game_state.generate_successor_gamestates()
    return [Node(self, game_state, self.depth + 1, self.use_g, self.use_h, self.use_f, self.heuristic) for game_state in successor_gamestates]
