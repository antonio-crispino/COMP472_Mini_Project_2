import random

ambulance = ['A', 'A']
cars = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
random_cars = []
random_puzzle_location = 'RandomPuzzles.txt'
report_location = 'Report.xls'

#TODO add fuel level
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
                    elif ((car_size == 3 and position+2 < len(board) and (board[position] == '.' and board[position+1] == '.' and board[position+2]) == '.')):
                        board[position] = car
                        board[position+1] = car
                        board[position+2] = car

                else:
                    # Add vertical cars
                    if (car_size == 2 and position+matrix_size < len(board) and board[position] == '.' and board[position+matrix_size] == '.'):
                        board[position] = car
                        board[position+matrix_size] = car
                    elif (car_size == 3 and (position+matrix_size*2) < len(board) and board[position] == '.' and board[position+matrix_size] == '.' and board[position+(2*matrix_size)] == '.'):
                        board[position] = car
                        board[position+matrix_size] = car
                        board[position+(matrix_size*2)] = car

    return board


def randomizeCars(car_amount):
    random_cars = set(random.sample(cars, car_amount))
    return random_cars


def addAmbulance(board, matrix_size):
    while True:
        # Chance of horizontal
        possible_pos = [i for i in range(len(board)) if board[i] == '.']
        ambulance_pos = random.choice(possible_pos)

        if (random.random() < 0.5):
            if ambulance_pos+1 < len(board) and board[ambulance_pos+1] == '.':
                board[ambulance_pos] = 'A'
                board[ambulance_pos+1] = 'A'
            # Chance of vertical
        else:
            if ambulance_pos+matrix_size < len(board) and board[ambulance_pos+matrix_size] == '.':
                board[ambulance_pos] = 'A'
                board[ambulance_pos+matrix_size] = 'A'
        if 'A' in board:
            break
    return board
    


def main():

    with open(random_puzzle_location, 'w+') as f:
        for i in range(50):
            random_puzzle = randomPuzzle(6, randomizeCars(10))
            game_puzzle = addAmbulance(random_puzzle, 6)
            input_string = ''.join(x for x in game_puzzle)+'\n'
            f.write(input_string)
            
        # TODO REPORT FORMAT


if __name__ == "__main__":
    main()
