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


def check_left (brd, move, length):
	return False


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

    pce, drc, num = move
    num = int(num)
    try:
    	assert (pce in in_brd)
		assert (pce != '.')
		assert (drc not in ('L','R', 'U', 'D'))
		long_brd = [item for row in brd for item in row]
		pos = long_brd.index(pce)
		row = pos/6
		col = pos%6
		if (long_brd[pos+1] == pce) and (drc in ('L', 'R')):
			if drc == 'L':
				assert (col - num >= 0)
			elif drc == 'R':
				if pce in lengths[2]:
					assert (col + num <= 4) 
				elif pce in lengths[3]:
					assert (col + num <= 3)
		elif (long_brd[pos+1] != pce) and (drc in ('U', 'D')):
			if drc == 'U':
				assert (row - num >= 0)
			elif drc == 'D':
				if pce in lengths[2]:
					assert (row + num <= 4) 
				elif pce in lengths[3]:
					assert (row + num <= 3)
		else:
			assert False

    	return True
    except:
	    return False


def read_player_input (brd):
    # FIX ME!

    in_brd = [item for row in brd for item in row]

    command = raw_input('Move name (or q)? ')
    if command == 'q':
    	exit(0)
    try:
        assert len(command) == 3
        assert (command[1].upper() in ('L','R', 'U', 'D'))
        assert (command[2] in ('1', '2', '3', '4'))
        move = tuple([c for c in command])
    except:
    	print 'Invalid input.'
        move = read_player_input(brd)

    if validate_move(brd, move):
        return move
	else:
		print 'Invalid move.'
		return read_player_input(brd)

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
    main()
