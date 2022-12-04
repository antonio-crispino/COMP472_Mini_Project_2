import os
from heuristic import Heuristic
from ucs_algorithm import UCSAlgorithm
from gbfs_algorithm import GBFSAlgorithm
from a_star_algorithm import AStarAlgorithm

def read_input_file(input_file_name):
  """
  Method to read input file of puzzles
  """
  puzzle_strings_list = []
  input_file_path =  os.path.join(os.getcwd(), "implementation", "input_files", input_file_name)
  with open(input_file_path, "r") as f:
    lines = f.readlines()
    for line in lines:
      line_clean = line.strip()
      if not (line_clean == "" or line_clean[0] == '#'):
        puzzle_strings_list.append(line_clean)
  return puzzle_strings_list

def create_output_files(subfolder, input_file_name, output_csv_name):
  """
  Method to create the output files of the puzzles
  """
  ucs_algorithm = "UCS"
  gbfs_algorithm = "GBFS"
  a_star_algorithm = "A/A*"

  ucs_string = "ucs"
  gbfs_string = "gbfs"
  a_star_string = "a"

  puzzle_strings = read_input_file(input_file_name)
  count = 0
  for puzzle_string in puzzle_strings:
    count += 1

    ## Don't re-run commented out code.

    # UCS
    ucs_1 = UCSAlgorithm(puzzle_string)
    ucs_1.search_for_solution()
    ucs_1.create_solution_and_search_files(subfolder + "\\" + ucs_string, ucs_string, None, count)
    ucs_1.add_to_csv_file(subfolder, output_csv_name, ucs_algorithm, "NA", count)

    # GBFS 1
    gbfs_1 = GBFSAlgorithm(puzzle_string, Heuristic.h1_number_of_blocking_vehicles)
    gbfs_1.search_for_solution()
    gbfs_1.create_solution_and_search_files(subfolder + "\\" + gbfs_string, gbfs_string, "h1", count)
    gbfs_1.add_to_csv_file(subfolder, output_csv_name, gbfs_algorithm, "h1", count)

    # GBFS 2
    gbfs_2 = GBFSAlgorithm(puzzle_string, Heuristic.h2_number_of_blocked_positions)
    gbfs_2.search_for_solution()
    gbfs_2.create_solution_and_search_files(subfolder + "\\" + gbfs_string, gbfs_string, "h2", count)
    gbfs_2.add_to_csv_file(subfolder, output_csv_name, gbfs_algorithm, "h2", count)

    # GBFS 3
    gbfs_3 = GBFSAlgorithm(puzzle_string, Heuristic.h3_number_of_blocking_vehicles_multiplied_by_constant_5)
    gbfs_3.search_for_solution()
    gbfs_3.create_solution_and_search_files(subfolder + "\\" + gbfs_string, gbfs_string, "h3", count)
    gbfs_3.add_to_csv_file(subfolder, output_csv_name, gbfs_algorithm, "h3", count)

     # GBFS 4
    gbfs_4 = GBFSAlgorithm(puzzle_string, Heuristic.h4_number_of_blocking_vehicles_multiplied_by_number_of_blocked_positions)
    gbfs_4.search_for_solution()
    gbfs_4.create_solution_and_search_files(subfolder + "\\" + gbfs_string, gbfs_string, "h4", count)
    gbfs_4.add_to_csv_file(subfolder, output_csv_name, gbfs_algorithm, "h4", count)

    # A/A* 1
    a_star_1 = AStarAlgorithm(puzzle_string, Heuristic.h1_number_of_blocking_vehicles)
    a_star_1.search_for_solution()
    a_star_1.create_solution_and_search_files(subfolder + "\\" + a_star_string, a_star_string, "h1", count)
    a_star_1.add_to_csv_file(subfolder, output_csv_name, a_star_algorithm, "h1", count)

    # A/A* 2
    a_star_2 = AStarAlgorithm(puzzle_string, Heuristic.h2_number_of_blocked_positions)
    a_star_2.search_for_solution()
    a_star_2.create_solution_and_search_files(subfolder + "\\" + a_star_string, a_star_string, "h2", count)
    a_star_2.add_to_csv_file(subfolder, output_csv_name, a_star_algorithm, "h2", count)

    # A/A* 3
    a_star_3 = AStarAlgorithm(puzzle_string, Heuristic.h3_number_of_blocking_vehicles_multiplied_by_constant_5)
    a_star_3.search_for_solution()
    a_star_3.create_solution_and_search_files(subfolder + "\\" + a_star_string, a_star_string, "h3", count)
    a_star_3.add_to_csv_file(subfolder, output_csv_name, a_star_algorithm, "h3", count)

    # A/A* 4
    a_star_4 = AStarAlgorithm(puzzle_string, Heuristic.h4_number_of_blocking_vehicles_multiplied_by_number_of_blocked_positions)
    a_star_4.search_for_solution()
    a_star_4.create_solution_and_search_files(subfolder + "\\" + a_star_string, a_star_string, "h4", count)
    a_star_4.add_to_csv_file(subfolder, output_csv_name, a_star_algorithm, "h4", count)

    break
  
### MAIN OUTPUT ###
# Create all of the output files from a given input file
# Must already have created folder structure and output csv file
# Created sample folder, a folder, gbfs folder, ucs folder, and sample_performance.csv file in this case (before running)
create_output_files("sample", "sample-input.txt", "performance.csv")
