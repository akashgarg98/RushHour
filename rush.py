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

def rotate_left (brd, rots):
    rotated = [row[:] for row in brd]
    span = range(len(brd))
    for i in range(rots):
        rotated = [[rotated[r][c] for r in span] for c in span[::-1]]
    return rotated

def check_left (brd, row, col, num, car_len):
    if col-num >= 0:
        path = brd[row][col-num:col]
        return (path == ['.']*len(path))
    return False

def check_right (brd, row, col, num, car_len):
    rotated_brd = rotate_left(brd, 2)
    return check_left(rotated_brd, 5-row, 6-car_len-col, num, car_len)

def check_up (brd, row, col, num, car_len):
    rotated_brd = rotate_left(brd, 1)
    return check_left(rotated_brd, 5-col, row, num, car_len)

def check_down (brd, row, col, num, car_len):
    rotated_brd = rotate_left(brd, 3)
    return check_left(rotated_brd, col, 6-car_len-row, num, car_len)

def validate_move (brd, move):
    # FIX ME!
    # check that piece is on the board
    # check that piece placed so it can move in that direction
    # check that piece would be in bound
    # check that path to target position is free

    lengths = {
                2:('X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'),
                3:('O', 'P', 'Q', 'R')
               }

    in_brd = [item for row in brd for item in row]

    pce, drc, num = move
    num = int(num)

    if pce in lengths[3]:
        car_len = 3
    else:
        car_len = 2

    try:
        assert (pce in in_brd)
        pos = in_brd.index(pce)
        row = pos/6
        col = pos%6
        assert (pce != '.')
        assert (drc in ('L', 'R', 'U', 'D'))
        if (in_brd[pos+1] == pce) and (drc in ('L', 'R')):
            if drc == 'L':
                assert (col - num >= 0)
                assert check_left(brd, row, col, num, car_len)
            elif drc == 'R':
                assert (col + num <= 6 - car_len)
                assert check_right(brd, row, col, num, car_len)
        elif (in_brd[pos+1] != pce) and (drc in ('U', 'D')):
            if drc == 'U':
                assert (row - num >= 0)
                assert check_up(brd, row, col, num, car_len)
            elif drc == 'D':
                assert (row + num <= 6 - car_len)
                assert check_down(brd, row, col, num, car_len) 
        else:
            assert False

        return True
    except:
        return False


def read_player_input (brd):

    command = raw_input('Move name (or q)? ')
    if command.upper() == 'Q':
        exit(0)
    try:
        assert len(command) == 3
        assert (command[1].upper() in ('L', 'R', 'U', 'D'))
        assert (command[2] in ('1', '2', '3', '4'))
        move = tuple([c for c in command.upper()])
    except:
        print 'Invalid input.'
        move = read_player_input(brd)

    if validate_move(brd, move):
        print move
        return move
    else:
        print 'Invalid move.'
        return read_player_input(brd)

def update_board (brd, move):

    lengths = {
                2:('X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'),
                3:('O', 'P', 'Q', 'R')
               }

    in_brd = [item for row in brd for item in row]

    pce, drc, num = move
    num = int(num)

    if pce in lengths[3]:
        car_len = 3
    else:
        car_len = 2

    pos = in_brd.index(pce)
    row = pos/6
    col = pos%6

    for i in range(car_len):
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


def print_board (brd):
    subprocess.call('cls' if platform.system() == 'Windows' else 'clear')
    for i, row in enumerate(brd):
        row_str = ' '.join(row)
        if i == 2:
            row_str += '  ===>'
        print row_str

    
def done (brd):
    return (brd[2][4] == 'X') and (brd[2][5] == 'X')


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
        brd = update_board(brd, move)
        print_board(brd)

    print 'YOU WIN! (Yay...)\n'
        

if __name__ == '__main__':
    import subprocess
    import platform
    main()
