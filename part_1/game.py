import numpy as np
from copy import copy, deepcopy

class GameState:
  '''
  The GameState class
  '''
  # Class variables
  grid_size = 6
  free_space = '.'
  ambulance = "A"
  axis = { "x": "x", "y": "y" }
  direction = { "l": "left", "r": "right", "u": "up", "d": "down" }

  def __init__(self, grid, vehicles, change):
    """
    The GameState Constructor
    """
    self.change = deepcopy(change)      # The change that led to this GameState
    self.vehicles = deepcopy(vehicles)  # The data of the vehicles (fuel and movable axis)
    self.grid = deepcopy(grid)          # The 2D grid representation (6x6) of the puzzle
    self.grid_string = ''.join(self.grid.reshape(GameState.grid_size ** 2))
    
    # TESTING
    # print()
    # print(self.grid)
    # print(self.change)
    # [print(key,':',value) for key, value in self.vehicles.items()]
    # print()
  
  def get_change(self):
    """
    Accessor: returns a deepcopy of the change object
    """
    return deepcopy(self.change)

  def get_vehicles(self):
    """
    Accessor: returns a deepcopy of the vehicles object
    """
    return deepcopy(self.vehicles)

  def get_grid(self):
    """
    Accessor: returns a deepcopy of the grid 2D-array
    """
    return deepcopy(self.grid)
  
  def get_grid_string_2d(self):
    """
    Method that returns the grid as a 2D string
    """
    grid_string_2d = ""
    for row in self.grid:
      grid_string_2d += ''.join(row) + "\n"
    return grid_string_2d[:-1]

  def get_fuel_amounts_string(self):
    """
    Method that returns the fuel amount for each vehicle
    """
    fuel_amounts_string = "Car fuel available: "
    for vehicle_name, vehicle_data in self.vehicles.items():
      fuel_amounts_string += vehicle_name + ":" + str(vehicle_data["fuel"]) + ", "
    return fuel_amounts_string[:-2]
  
  def get_change_string(self):
    """
    Method that returns the GameState change as a string
    """
    if (self.change["vehicle_moved"] == None):
      return '%-18s' % ("Initial")
    else:
      return '%s %5s %s' % (
        self.change["vehicle_moved"],
        self.change["direction_moved"],
        self.change["distance_moved"])

  def get_data_string(self):
    """
    Method that returns a data representation of the GameState as a string
    """
    if (self.change["vehicle_moved"] == None):
      return '%s %s' % (self.get_change_string(), self.grid_string)
    else:
      return '%s %8s %s' % (
        self.get_change_string(),
        self.change["fuel_remaining"],
        self.grid_string)
  
  @classmethod
  def generate_initial_gamestate(cls, puzzle_string):
    """
    Class method that creates the first GameState
    """
    # Get puzzle grid, vehicle names, vehicle fuel, and vehicle moveable axis)
    puzzle_components = puzzle_string.split()
    grid_string = puzzle_components[0]
    grid_array_1d = np.array(list(grid_string))
    grid_array_2d = grid_array_1d.reshape(cls.grid_size, cls.grid_size)
    vehicle_names = sorted(list(set(grid_string)))[1:]
    vehicle_fuel_amounts_given = {fuel[0]: int(fuel[1:]) for fuel in puzzle_components[1:]}
    vehicles_data = {vehicle_name: {} for vehicle_name in vehicle_names}
    
    # Set up the change object (all attributes equal to None because this is the initial state)
    change_data = {
      "vehicle_moved": None,
      "direction_moved": None,
      "distance_moved": None,
      "fuel_remaining": None,
      "is_solution_state": False}

    ### Initialize the vehicle data
    for vehicle_name, vehicle_data in vehicles_data.items():

      ## Add the amount of fuel to each vehicle
      # If the fuel amount is given, add that amount
      if (vehicle_name in vehicle_fuel_amounts_given):
        vehicle_data["fuel"] = vehicle_fuel_amounts_given[vehicle_name]
      # Otherwise, add the amount of 100
      else:
        vehicle_data["fuel"] = 100

      ## Add the moveable axis of each vehicle
      vehicle_positions = [
        (position//cls.grid_size, position%cls.grid_size) 
        for position in np.where(grid_array_1d == vehicle_name)[0]
      ]
      # If all y values are the same, then the vehicle can move on the x-axis
      if (all(position[0] == vehicle_positions[0][0] for position in vehicle_positions)):
        vehicle_data["axis"] = cls.axis["x"]
      # Otherwise if all x values are the same, then the vehicle can move on the y-axis
      else:
        vehicle_data["axis"] = cls.axis["y"]
      
      ## Add the positions for each vehicle
      vehicle_data["positions"] = vehicle_positions

    return GameState(grid_array_2d, vehicles_data, change_data)

  def generate_successor_gamestates(self):
    """
    Method that creates the child GameStates of the GameState
    """
    # Container to hold successor states
    successor_gamestates = []

    # For each vehicle, do the following
    for vehicle_name, vehicle_data in self.vehicles.items():

      # Proceed only if the vehicle has fuel and it remains in the grid (may have been removed due to valet service extraction)
      if (vehicle_data["fuel"] > 0 and len(vehicle_data["positions"]) > 0):
        # Set the change data (vehicle name and remaining fuel amount)
        change_new = self.get_change()
        change_new["vehicle_moved"] = copy(vehicle_name)
        change_new["fuel_remaining"] = copy(vehicle_data["fuel"]) - 1

        # If the vehicle axis is x
        if (vehicle_data["axis"] == GameState.axis["x"]):

          # LEFT DIRECTION
          distance = 0
          x_position_new = copy(vehicle_data["positions"][0][1]) - 1
          y_position = copy(vehicle_data["positions"][0][0])
          vehicles_new = self.get_vehicles()
          grid_new = self.get_grid()
          # Set the change data (direction moved)
          change_new["direction_moved"] = GameState.direction["l"]
          # While there are free positions to the left of the vehicle, do the following
          while (x_position_new >= 0 and self.grid[y_position, x_position_new] == GameState.free_space):
            # Set the change data (distance moved)
            distance += 1
            change_new["distance_moved"] = copy(distance)
            # Modify the grid to reflect the vehicle movement
            grid_new[y_position, x_position_new] = copy(vehicle_name)
            grid_new[y_position, vehicles_new[vehicle_name]["positions"][-1][1]] = GameState.free_space
            # Modify the vehicle positions to reflect the vehicle movement
            vehicles_new[vehicle_name]["positions"].pop(-1)
            vehicles_new[vehicle_name]["positions"].insert(0, (copy(y_position), copy(x_position_new)))
            # Change the new position for the next round
            x_position_new -= 1
            # Create a GameState object and append it to the container that holds successor states
            successor_gamestates.append(GameState(grid_new, vehicles_new, change_new))

          # RIGHT DIRECTION
          distance = 0
          x_position_new = copy(vehicle_data["positions"][-1][1]) + 1
          y_position = copy(vehicle_data["positions"][-1][0])
          vehicles_new = self.get_vehicles()
          grid_new = self.get_grid()
          # Set the change data (direction moved)
          change_new["direction_moved"] = GameState.direction["r"]
          # While there are free positions to the right of the vehicle, do the following
          while (x_position_new < 6 and self.grid[y_position, x_position_new] == GameState.free_space):
            # Set the change data (distance moved)
            distance += 1
            change_new["distance_moved"] = copy(distance)
            # If the vehicle reaches the exit door and is not an ambulance "A" (must be moveable on the "x" axis and moving in the "right" direction)
            if (y_position == 2 and x_position_new == 5 and vehicle_name != GameState.ambulance):
              # Modify the grid to reflect the vehicle movement (valet service extraction)
              for position in vehicles_new[vehicle_name]["positions"]:
                grid_new[position[0], position[1]] = GameState.free_space
              # Modify the vehicle positions to reflect the vehicle movement (valet service extraction)
              vehicles_new[vehicle_name]["positions"].clear()
            else:
              # Modify the grid to reflect the vehicle movement
              grid_new[y_position, x_position_new] = copy(vehicle_name)
              grid_new[y_position, vehicles_new[vehicle_name]["positions"][0][1]] = GameState.free_space
              # Modify the vehicle positions to reflect the vehicle movement
              vehicles_new[vehicle_name]["positions"].pop(0)
              vehicles_new[vehicle_name]["positions"].append((copy(y_position), copy(x_position_new)))
              # If the vehicle reaches the exit door and is an ambulance "A"
              if (y_position == 2 and x_position_new == 5 and vehicle_name == GameState.ambulance):
                change_new["is_solution_state"] = True
                
            # Change the new position for the next round
            x_position_new += 1
            # Create a GameState object and append it to the container that holds successor states
            successor_gamestates.append(GameState(grid_new, vehicles_new, change_new))
        
        # If the vehicle axis is y
        # if (vehicle_data["axis"] == GameState.axis["y"]):
        else:
          
          # UP DIRECTION
          distance = 0
          x_position = copy(vehicle_data["positions"][0][1])
          y_position_new = copy(vehicle_data["positions"][0][0]) - 1
          vehicles_new = self.get_vehicles()
          grid_new = self.get_grid()
          # Set the change data (direction moved)
          change_new["direction_moved"] = GameState.direction["u"]
          # While there are free positions to the left of the vehicle, do the following
          while (y_position_new >= 0 and self.grid[y_position_new, x_position] == GameState.free_space):
            # Set the change data (distance moved)
            distance += 1
            change_new["distance_moved"] = copy(distance)
            # Modify the grid to reflect the vehicle movement
            grid_new[y_position_new, x_position] = copy(vehicle_name)
            grid_new[vehicles_new[vehicle_name]["positions"][-1][0], x_position] = GameState.free_space
            # Modify the vehicle positions to reflect the vehicle movement
            vehicles_new[vehicle_name]["positions"].pop(-1)
            vehicles_new[vehicle_name]["positions"].insert(0, (copy(y_position_new), copy(x_position)))
            # Change the new position for the next round
            y_position_new -= 1
            # Create a GameState object and append it to the container that holds successor states
            successor_gamestates.append(GameState(grid_new, vehicles_new, change_new))

          # DOWN DIRECTION
          distance = 0
          x_position = copy(vehicle_data["positions"][-1][1])
          y_position_new = copy(vehicle_data["positions"][-1][0]) + 1
          vehicles_new = self.get_vehicles()
          grid_new = self.get_grid()
          # Set the change data (direction moved)
          change_new["direction_moved"] = GameState.direction["d"]
          # While there are free positions to the right of the vehicle, do the following
          while (y_position_new < 6 and self.grid[y_position_new, x_position] == GameState.free_space):
            # Set the change data (distance moved)
            distance += 1
            change_new["distance_moved"] = copy(distance)
            # Modify the grid to reflect the vehicle movement
            grid_new[y_position_new, x_position] = copy(vehicle_name)
            grid_new[vehicles_new[vehicle_name]["positions"][0][0], x_position] = GameState.free_space
            # Modify the vehicle positions to reflect the vehicle movement
            vehicles_new[vehicle_name]["positions"].pop(0)
            vehicles_new[vehicle_name]["positions"].append((copy(y_position_new), copy(x_position)))
            # Change the new position for the next round
            y_position_new += 1
            # Create a GameState object and append it to the container that holds successor states
            successor_gamestates.append(GameState(grid_new, vehicles_new, change_new))
    
    return successor_gamestates
