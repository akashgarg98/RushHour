#!/usr/bin/env python
import subprocess
import platform

#
# Game Programming, Level 1 Project
#
# RUSH HOUR
#
# A simple puzzle game, based on the physical game of the same name 
# by Binary Arts Corp
#
# Devs: Jacob Kingery
#       Philip Seger

def fail (msg):
    raise StandardError(msg)

def get_length(pce):
    '''
    Return the length of the specified pce.
    '''
    lengths = {2:('XABCDEFGHIJK'), 3:('OPQR')}

    if pce in lengths[3]:
        return 3
    elif pce in lengths[2]:
        return 2
    else:
        fail('Invalid piece name.')

GRID_SIZE = 6

def rotate_left (brd, rots):
    '''
    Rotate brd (a n by n nested list) to the left rots times.
    '''
    rotated = [row[:] for row in brd]
    span = range(len(brd))
    for i in range(rots):
        rotated = [[rotated[r][c] for r in span] for c in span[::-1]]
    return rotated

def check_left (brd, row, col, num, car_len):
    '''
    Check if the piece at (row, col) with length 
    car_len can move to the left num spaces.
    '''
    if col-num >= 0:
        path = brd[row][col-num:col]
        return (path == ['.']*len(path))
    return False

def check_right (brd, row, col, num, car_len):
    '''
    Check if the piece at (row, col) with length 
    car_len can move to the right num spaces.
    '''
    rotated_brd = rotate_left(brd, 2)
    # Coordinates must be rotated to match the board's new orientation
    return check_left(rotated_brd, 5-row, 6-car_len-col, num, car_len) 

def check_up (brd, row, col, num, car_len):
    '''
    Check if the piece at (row, col) with length 
    car_len can move up num spaces.
    '''
    rotated_brd = rotate_left(brd, 1)
    # Coordinates must be rotated to match the board's new orientation
    return check_left(rotated_brd, 5-col, row, num, car_len)

def check_down (brd, row, col, num, car_len):
    '''
    Check if the piece at (row, col) with length 
    car_len can move down num spaces.
    '''
    rotated_brd = rotate_left(brd, 3)
    # Coordinates must be rotated to match the board's new orientation
    return check_left(rotated_brd, col, 6-car_len-row, num, car_len)

def validate_move (brd, move):
    '''
    Check that the piece specified in move is in brd, can move in 
    the direction specified in move, would be in bounds after moving,
    and has a clear path to the desired position.
    '''

    in_brd = [item for row in brd for item in row]

    pce, drc, num = move
    num = int(num)

    car_len = get_length(pce)

    try:
        assert (pce in in_brd)  # Continue if piece is in board

        pos = in_brd.index(pce)
        row = pos/6
        col = pos%6
        
        assert (pce != '.')  # Continue if piece is not .

        assert (drc in ('L', 'R', 'U', 'D'))  # Continue if direction is valid

        if (in_brd[pos+1] == pce) and (drc in ('L', 'R')):
            # If the space to the right is a piece of the same letter,
            # the piece can only move horizontally
            if drc == 'L':
                assert (col - num >= 0)  # Continue if move will be in bounds
                assert check_left(brd, row, col, num, car_len)
            elif drc == 'R':
                assert (col + num <= 6 - car_len)  # Continue if move will be in bounds
                assert check_right(brd, row, col, num, car_len)

        elif (in_brd[pos+1] != pce) and (drc in ('U', 'D')):
            # If the space to the right is not a piece of the same letter,
            # the piece can only move vertically
            if drc == 'U':
                assert (row - num >= 0)  # Continue if move will be in bounds
                assert check_up(brd, row, col, num, car_len)
            elif drc == 'D':
                assert (row + num <= 6 - car_len)  # Continue if move will be in bounds
                assert check_down(brd, row, col, num, car_len) 

        else:
            assert False

        return True  # Move passed tests and is valid
    except:
        return False  # Move failed tests and is invalid


def read_player_input (brd):
    '''
    Get command from player, do preliminary 
    validation, and do full validation.
    '''
    command = raw_input('Move name (or q)? ')

    if command.upper() == 'Q':
        exit(0)  # Quit on q or Q

    try:
        assert len(command) == 3  # Continue if command is correct length
        assert (command[1].upper() in ('L', 'R', 'U', 'D'))  # Continue if direction is valid
        assert (command[2] in ('1', '2', '3', '4'))  # Continue if distance is possibly valid
        move = tuple([c for c in command.upper()])  # Package as tuple
    except:
        print 'Invalid input.'
        move = read_player_input(brd)  # If invalid input, ask for a new move

    if validate_move(brd, move):
        return move
    else:
        print 'Invalid move.'
        return read_player_input(brd)  # If invalid move, ask for a new move

def update_board (brd, move):
    '''
    Update brd to reflect validated move.
    '''
    in_brd = [item for row in brd for item in row]

    pce, drc, num = move
    num = int(num)

    car_len = get_length(pce)

    pos = in_brd.index(pce)
    row = pos/6
    col = pos%6

    for i in range(car_len):
        # Write . over old positions and pce over new positions
        if drc == 'L':
            brd[row][col+i] = '.'
            brd[row][col+i-num] = pce
        elif drc == 'R':
            brd[row][col-i+car_len-1] = '.'
            brd[row][col-i+car_len-1+num] = pce
        elif drc == 'U':
            brd[row+i][col] = '.'
            brd[row+i-num][col] = pce
        elif drc == 'D':
            brd[row-i+car_len-1][col] = '.'
            brd[row-i+car_len-1+num][col] = pce

    return brd


def print_board (brd, score):
    '''
    Clear terminal and print out board.
    '''
    subprocess.call('cls' if platform.system() == 'Windows' else 'clear')
    print 'Current score: ' + str(score)
    for i, row in enumerate(brd):
        row_str = ' '.join(row)
        if i == 2:
            row_str += '  ===>'
        print row_str

    
def done (brd):
    '''
    Check if X piece is in winning position.
    '''
    return (brd[2][4] == 'X') and (brd[2][5] == 'X')


def create_initial_level ():
    '''
    Create initial hard-coded board.
    '''
    initial_board = [['.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.'],
                     ['.', 'X', 'X', 'O', '.', '.'],
                     ['.', 'A', 'A', 'O', '.', 'P'],
                     ['.', 'B', '.', 'O', '.', 'P'],
                     ['.', 'B', 'C', 'C', '.', 'P']]

    return initial_board

def create_custom_level (layout):
    '''
    Create initial board using user generated layout.
    '''
    initial_board = [['.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.']]
    for i in range(len(layout)/4):
        car = layout[4*i:4*i+4]

        pce = car[0].upper()
        drc = car[3].upper()
        col = int(car[1]) - 1
        row = int(car[2]) - 1

        car_len = get_length(pce)

        for i in range(car_len):
            if drc == 'R':
                initial_board[row][col+i] = pce
            elif drc == 'D':
                initial_board[row+i][col] = pce

    return initial_board

def main (layout = False):
    '''
    Create and print initial board, then begin gameplay loop of
    getting player input, updating board, and printing board.
    '''
    score = 0
    if layout:
        brd = create_custom_level(layout)
    else:
        brd = create_initial_level()

    print_board(brd, score)

    while not done(brd):
        move = read_player_input(brd)
        brd = update_board(brd, move)
        score += 1
        print_board(brd, score)

    print 'YOU WIN! (Yay...)\n'
        

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
    	main(sys.argv[1])
    else:
    	main()