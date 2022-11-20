import numpy as np

class Game:
  '''
  The Game class
  '''
  def __init__(self, puzzle_string):
    """
    The Game Constructor
    Initializes the game with the first GameState
    """
    # Get puzzle components (grid, free spaces, fuel, characters and vehicle names)
    puzzle_components = puzzle_string.split()
    puzzle_grid_string = puzzle_components[0]
    puzzle_grid_array_1d = np.array(list(puzzle_grid_string))
    puzzle_grid_array_2d = puzzle_grid_array_1d.reshape(GameState.grid_size,GameState.grid_size)
    puzzle_fuel_amounts_given = {fuel[0]: int(fuel[1:]) for fuel in puzzle_components[1:]}
    puzzle_characters = [chr(number) for number in range(ord('A'), ord('Z')+1) if chr(number) in puzzle_grid_string]
    puzzle_vehicles = {character_name: {} for character_name in puzzle_characters}

    # Initialize the vehicle data
    for vehicle_name, vehicle_data in puzzle_vehicles.items():
      # Add the amount of fuel to each vehicle
      if (vehicle_name in puzzle_fuel_amounts_given):
        vehicle_data["fuel"] = puzzle_fuel_amounts_given[vehicle_name]
      else:
        vehicle_data["fuel"] = 100
      # Add the moveable axis of each vehicle
      puzzle_vehicle_positions = GameState.get_character_positions(puzzle_grid_array_1d, vehicle_name)
      if (all(position[0] == puzzle_vehicle_positions[0][0] for position in puzzle_vehicle_positions)):
        vehicle_data["axis"] = GameState.axis["x"]
      else:
        vehicle_data["axis"] = GameState.axis["y"]

    # Save the initial GameState object as an instance variable
    self.initial_game_state = GameState(puzzle_grid_array_2d, puzzle_vehicles)

class GameState:
  '''
  The GameState class
  '''
  # Class variables
  axis = { "x": "x", "y": "y" }
  direction = { "l": "left", "r": "right", "u": "up", "d": "down" }
  grid_size = 6

  def __init__(self, puzzle_array_2d, vehicles, vehicle_moved = None, direction_moved = None, amount_moved = None):
    """
    The GameState Constructor
    """
    self.vehicle_moved = vehicle_moved
    self.direction_moved = direction_moved
    self.amount_moved = amount_moved
    self.puzzle_array_2d = puzzle_array_2d.copy()
    self.puzzle_array_1d = self.puzzle_array_2d.reshape(GameState.grid_size*GameState.grid_size)
    self.puzzle_string = ''.join(self.puzzle_array_1d)
    self.free_space_positions = GameState.get_character_positions(self.puzzle_array_1d, '.')
    self.vehicles = vehicles
    self.vehicle_positions = {vehicle: GameState.get_character_positions(self.puzzle_array_1d, vehicle) for vehicle in self.vehicles}
    self.vehicle_free_space_positions = {vehicle: {} for vehicle in self.vehicles}
    self.get_free_reachable_spaces_for_all_vehicles()

    # self.get_all_successors()
    self.print_gamestate()
    
  def get_free_reachable_spaces_for_all_vehicles(self):
    """
    Creates a dictionary of all the free spaces that are reachable by each vehicle
    It considers their moveable axis and their fuel capacity
    """
    for vehicle_name, vehicle_data in self.vehicles.items():
      # Get the direction and shifts of the vehicle
      direction = None
      shifts = None
      if (vehicle_data["axis"] == GameState.axis["x"]):
        direction = 1 # x-axis
        shifts = [GameState.direction["l"], GameState.direction["r"]] # left and right
      else:
        direction = 0 # y-axis
        shifts = [GameState.direction["d"], GameState.direction["u"]] # down and up
      
      # Get the direction and shifts of the vehicle
      self.vehicle_free_space_positions[vehicle_name][shifts[0]] = []
      self.vehicle_free_space_positions[vehicle_name][shifts[1]] = []

      # Get the possible new starting and ending positions of the vehicle
      new_start_position = list(self.vehicle_positions[vehicle_name][0])
      new_end_position = list(self.vehicle_positions[vehicle_name][-1])
      new_start_position[direction] -= 1
      new_end_position[direction] += 1

      # loop left or upwards and get the free positions until a non-free space is found or no fuel remains
      vehicle_fuel = vehicle_data["fuel"] # To keep track of fuel consumed by the vehicle to get to a specific position
      distance = 1 # To keep track of distance travelled by the vehicle to get to a specific position
      while ((tuple(new_start_position) in self.free_space_positions) and vehicle_fuel > 0): # Max 4 iterations (size 6 - max vehicle length 2)
        self.vehicle_free_space_positions[vehicle_name][shifts[0]].insert(0, {"pos": tuple(new_start_position), "dist": distance})
        new_start_position[direction] -= 1
        vehicle_fuel -= 1
        distance += 1
      
      # loop right or downwards and get the free positions until a non-free space is found or no fuel remains
      vehicle_fuel = vehicle_data["fuel"] # To keep track of fuel consumed by the vehicle to get to a specific position
      distance = 1 # To keep track of distance travelled by the vehicle to get to a specific position
      while ((tuple(new_end_position) in self.free_space_positions) and vehicle_fuel > 0): # Max 4 iterations (size 6 - max vehicle length 2)
        self.vehicle_free_space_positions[vehicle_name][shifts[1]].append({"pos": tuple(new_end_position), "dist": distance})
        new_end_position[direction] += 1
        vehicle_fuel -= 1
        distance += 1

  @staticmethod
  def get_character_positions(array_1d, character):
    return [(position//GameState.grid_size, position%GameState.grid_size) for position in np.where(array_1d == character)[0]]

  def print_gamestate(self):
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("---------------------------------------------------------")
    print("vehicle_moved:", self.vehicle_moved)
    print("direction_moved:", self.direction_moved)
    print("amount_moved:", self.amount_moved)
    print("---------------------------------------------------------")
    print("vehicles:")
    [print(key,':',value) for key, value in self.vehicles.items()]
    print("---------------------------------------------------------")
    print("puzzle_string:", self.puzzle_string)
    print("---------------------------------------------------------")
    print("puzzle_array_2d:\n", self.puzzle_array_2d)
    print("---------------------------------------------------------")
    print("free_space_positions:\n", self.free_space_positions)
    print("---------------------------------------------------------")
    print("vehicle_positions:")
    [print(key,':',value) for key, value in self.vehicle_positions.items()]
    print("---------------------------------------------------------")
    print("vehicle_free_space_positions:")
    [print(key,':',value) for key, value in self.vehicle_free_space_positions.items()]
    print("---------------------------------------------------------")

game = Game("AAB...C.BHH.C.RRDF....DFEEGGG....... C3 B4 H1 F2")
