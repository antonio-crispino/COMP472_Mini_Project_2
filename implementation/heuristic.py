from game_state import GameState

class Heuristic:
  '''
  The Heuristic class
  '''

  @classmethod
  def h1_number_of_blocking_vehicles(cls, game_state): # TESTED
    # Admissible
    """
    Heuristic function to get the number of blocking vehicles
    """
    return len(set(cls.get_blocked_positions_list(game_state)))

  @classmethod
  def h2_number_of_blocked_positions(cls, game_state): # TESTED
    # Not admissible
    """
    Heuristic function to get the number of blocked positions
    """
    return len(cls.get_blocked_positions_list(game_state))

  @classmethod
  def h3_number_of_blocking_vehicles_multiplied_by_constant_5(cls, game_state): # TESTED
    # Not admissible
    """
    Heuristic function to get the number of blocking vehicles multiplied by a constant (5 in this case)
    """
    return len(set(cls.get_blocked_positions_list(game_state))) * 5

  @classmethod
  def h4_number_of_blocking_vehicles_multiplied_by_number_of_blocked_positions(cls, game_state): # TESTED
    # Not admissible
    """
    Heuristic function to get the number of blocking vehicles multiplied by the number of blocked positions
    """
    return cls.h1_number_of_blocking_vehicles(game_state) * cls.h2_number_of_blocked_positions(game_state)
  
  # Helper method
  @classmethod
  def get_blocked_positions_list(cls, game_state): # TESTED
    """
    Method to get a list of the blocking positions (non free-space) between the ambulance and the exit door
    """
    grid = game_state.get_grid()
    vehicle_a = game_state.get_vehicles()[GameState.ambulance]
    blocked_positions = []
    # from the position of the side of the ambulance closest to the door to the position of the door
    y_position = vehicle_a["positions"][-1][0]
    for x_position in range(vehicle_a["positions"][-1][1] + 1, GameState.grid_size):
      if (grid[y_position, x_position] != GameState.free_space):
        blocked_positions.append(grid[y_position, x_position])
    return blocked_positions
