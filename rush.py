#!/usr/bin/env python

#
# Game Programming, Level 1 Project
#
# RUSH HOUR
#
# A simple puzzle game, based on the physical game of the same name 
# by Binary Arts Corp
#



# fail somewhat gracefully

def fail (msg):
    raise StandardError(msg)


GRID_SIZE = 6


def validate_move (brd, move):
    # FIX ME!
    # check that piece is on the board
    # check that piece placed so it can move in that direction
    # check that piece would be in bound
    # check that path to target position is free
    return False


def read_player_input (brd):
    # FIX ME!

    in_brd = []
    for row in brd:
        for cell in row:
            in_brd.append(cell)
    in_brd = set(in_board)

    command = raw_input('Move name (or q)? ')
    try:
        assert len(command) == 3
        assert (command[0].upper() in in_brd)
        #assert (command[0] != '.')
        #assert (command[1].upper() not in ('L','R', 'U', 'D'))
        #assert (command[2] not in ('1', '2', '3', '4'))
        move = command
    except:
        move = read_player_input(brd)

    move = validate_move(brd, move)

    return move


def update_board (brd,move):
    # FIX ME!
    return brd


def print_board (brd):

    for i, row in enumerate(brd):
        row_str = ' '.join(row)
        if i == 2:
            row_str += '  ===>'
        print row_str

    
def done (brd):
    # FIX ME!
    return True


# initial board:
# Board positions (1-6,1-6), directions 'r' or 'd'
#
# X @ (2,3) r
# A @ (2,4) r
# B @ (2,5) d
# C @ (3,6) r
# O @ (4,3) d
# P @ (6,4) d


def create_initial_level ():
    initial_board = [['.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.'],
                     ['.', 'X', 'X', 'O', '.', '.'],
                     ['.', 'A', 'A', 'O', '.', 'P'],
                     ['.', 'B', '.', 'O', '.', 'P'],
                     ['.', 'B', 'C', 'C', '.', 'P']]

    return initial_board


def main ():

    brd = create_initial_level()

    print_board(brd)

    while not done(brd):
        move = read_player_input(brd)
        brd = update_board(brd,move)
        print_board(brd)

    print 'YOU WIN! (Yay...)\n'
        

if __name__ == '__main__':
    main()
