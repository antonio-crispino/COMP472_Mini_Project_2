import random

### This file was kept but is not necessary for the submission, can be ignored ###

cars = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
random_puzzle_file_location = 'RandomPuzzles.txt'
report_file_location = 'Report.xlsx'
test_input = 'test.txt'

def randomPuzzle(matrix_size, random_cars):
    board = [('.') for i in range(matrix_size * matrix_size)]
    # Shuffle indices for random starting point
    matrix_indices = list(range(len(board)))
    random.shuffle(matrix_indices)
    for position in matrix_indices:
        for car in random_cars:
            if car not in board:
                # Choose random size
                car_size = random.randint(2, 3)
                # Choose between horizontal or vertical
                if (random.random() < 0.5):
                    # Add horizontal cars
                    if (car_size == 2 and position+1 < len(board) and (board[position] == '.' and board[position+1] == '.')):
                        board[position] = car
                        board[position+1] = car
                        board.extend(add_fuel(car))
                     
                    elif ((car_size == 3 and position+2 < len(board) and (board[position] == '.' and board[position+1] == '.' and board[position+2]) == '.')):
                        board[position] = car
                        board[position+1] = car
                        board[position+2] = car
                        board.extend(add_fuel(car))
                else:
                    # Add vertical cars
                    if (car_size == 2 and position+matrix_size < len(board) and board[position] == '.' and board[position+matrix_size] == '.'):
                        board[position] = car
                        board[position+matrix_size] = car
                        board.extend(add_fuel(car))
                        
                    elif (car_size == 3 and (position+matrix_size*2) < len(board) and board[position] == '.' and board[position+matrix_size] == '.' and board[position+(2*matrix_size)] == '.'):
                        board[position] = car
                        board[position+matrix_size] = car
                        board[position+(matrix_size*2)] = car
                        board.extend(add_fuel(car))
    return board

def randomizeCars():
    # Randomize cars and number of cars for each puzzle
    random_cars = set(random.sample(cars, random.randint(5,10)))
    return random_cars

def add_fuel(car):
    if (random.random() < 0.5):
        return [' ', car+str(random.randint(1,100))]
    return ''

def addAmbulance(board):
    while True:
        # Possibility of ambulance position (3rd row)
        ambulance_pos = random.randint(12,17)
        board[ambulance_pos] = 'A'
        board[ambulance_pos+1] = 'A'     
        if 'A' in board:
            break
    return board
    
def generate_puzzles(num):
    with open(random_puzzle_file_location, 'w+') as f:
        for i in range(num):
            random_puzzle = randomPuzzle(6, randomizeCars())
            game_puzzle = addAmbulance(random_puzzle, 6)
            input_string = ''.join(x for x in game_puzzle)+'\n'
            f.write(input_string)

def main():
    generate_puzzles(50)
