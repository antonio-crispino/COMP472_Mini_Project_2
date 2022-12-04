# COMP 472 Mini-Project 2

## URL of the GitHub Repository

https://github.com/antonio-crispino/COMP472_Mini_Project_2

## Team Members

| Team Member             | ID       |
| ----------------------- | -------- |
| Maira Malhi (Team Lead) | 40128269 |
| Antonio Crispino        | 40109690 |
| Nabila Mehreen          | 40130897 |

## Instructions on How to Run the Program

1. Clone the repository using the provided link.
2. Open the project folder using an IDE (VSCode or PyCharm).
3. Ensure that you have the necessary libraries that are not part of Python's standard library. (This includes numpy.)
4. Open the `main.py` file and run the `create_output_files` method to generate all the necessary output files given an input file. Given an input file of puzzle(s), the search, solution, and performance of each algorithm (and each heuristic) performed on each puzzle will be generated. The method takes three parameters:
    1. The first parameter is the `subfolder`. This is the name of the folder that is nested in the `output_files` folder. If you would like to output to a different folder than the ones already provided, simply create a new folder in the `output_files` folder before referencing it in the parameter. *It is important to note that when creating a subfolder, it must include three nested folders of its own named `ucs`, `gbfs`, and `a` respectively. It must also contain a csv file for the performance metrics (which can be named `performance.csv` but this is not mandatory).*
    2. The second parameter is the `input_file_name`. This is the name of the input text file that contains the puzzles, which must be nested within the `input_files` folder.
    3. The third parameter is the `output_csv_name`. This is the name of the output csv file that will contain the performance metrics of the algorithms called on the puzzles.
5. Once the program terminates execution, the output files can be observed and analysed.
