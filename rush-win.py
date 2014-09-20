#!/usr/bin/env python
import subprocess
import platform
import graphics as gr
import time
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
#
# For moving a block, use blockname, direction, and number
# 					i.e. ou2
#
# Assignment comments:
# Good pace of the project, and starting with just a command line
# implementation really helped visualize how the gui would later work

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


def read_player_input (brd, gr_obs):
    '''
    Get command from player, do preliminary 
    validation, and do full validation.
    '''
    # command = raw_input('Move name (or q)? ')
    e = gr_obs['entry']
    w = gr_obs['warning']

    while gr_obs['win'].checkKey() != 'Return':
        time.sleep(.1)

    command = e.getText()
    e.setText('')

    if command.upper() == 'Q':
        exit(0)  # Quit on q or Q

    try:
        assert len(command) == 3  # Continue if command is correct length
        assert (command[1].upper() in ('L', 'R', 'U', 'D'))  # Continue if direction is valid
        assert (command[2] in ('1', '2', '3', '4'))  # Continue if distance is possibly valid
        move = tuple([c for c in command.upper()])  # Package as tuple
    except:
        w.setText('Invalid input.')
        move = read_player_input(brd, gr_obs)  # If invalid input, ask for a new move

    if validate_move(brd, move):
        return move
    else:
        w.setText('Invalid move.')
        return read_player_input(brd, gr_obs)  # If invalid move, ask for a new move

def update_board (brd, move, gr_obs):
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

    dx, dy = 0, 0

    for i in range(car_len):
        # Write . over old positions and pce over new positions
        if drc == 'L':
            dx = -70
            brd[row][col+i] = '.'
            brd[row][col+i-num] = pce
        elif drc == 'R':
            dx = 70
            brd[row][col-i+car_len-1] = '.'
            brd[row][col-i+car_len-1+num] = pce
        elif drc == 'U':
            dy = -70
            brd[row+i][col] = '.'
            brd[row+i-num][col] = pce
        elif drc == 'D':
            dy = 70
            brd[row-i+car_len-1][col] = '.'
            brd[row-i+car_len-1+num][col] = pce

    car_ob = gr_obs[pce]
    for ob in car_ob:
        ob.move(dx*num, dy*num)

    return brd


def render_initial_board (brd, score):
    '''
    Clear terminal, print out board, and show current score.
    '''
    span = range(len(brd))
    gr_obs = dict()

    win = gr.GraphWin('Game Board', 500, 500, autoflush=False)
    gr_obs['win'] = win

    for i in span:
        for j in span:
            r = gr.Rectangle(gr.Point(10+70*i,10+70*j), gr.Point(70*(i+1),70*(j+1)))
            r.draw(win)
    
    t = gr.Text(gr.Point(460, 180), 'EXIT')
    t.setSize(24)
    t.setTextColor('red')
    t.draw(win)    

    s = gr.Text(gr.Point(480, 490), score)
    s.setSize(18)
    s.setTextColor('blue')
    s.draw(win)
    gr_obs['score'] = s

    e = gr.Entry(gr.Point(250, 480), 5)
    e.draw(win)
    gr_obs['entry'] = e

    w = gr.Text(gr.Point(250, 450), '')
    w.draw(win)
    gr_obs['warning'] = w

    in_brd = [item for row in brd for item in row]
    brd_set = set(in_brd)
    brd_set.discard('.')


    for pce in brd_set:
        car_len = get_length(pce)

        pos = in_brd.index(pce)
        row = pos/6
        col = pos%6

        if (in_brd[pos+1] == pce):
            c = gr.Rectangle(gr.Point(10+70*col,10+70*row), gr.Point(70*(col+car_len), 70*(row+1)))
        else:
            c = gr.Rectangle(gr.Point(10+70*col,10+70*row), gr.Point(70*(col+1), 70*(row+car_len)))

        if pce == 'X':
            c.setFill('red')
        elif car_len == 2:
            c.setFill('blue')
        else:
            c.setFill('green')
        l = gr.Text(c.getCenter(), pce)
        c.draw(win)
        l.draw(win)
        gr_obs[pce] = (c, l) 

    win.update()

    return gr_obs

def done (brd):
    '''
    Check if X piece is in winning position.
    '''
    return (brd[2][4] == 'X') and (brd[2][5] == 'X')

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

def main (layout=False):
    '''
    Create and print initial board, then begin gameplay loop of
    getting player input, updating board, and printing board.
    '''
    score = 0 # score used for number of moves (less is better)
    layout = layout if layout else 'X23rA24rB25dC36rO43dP64d'
    brd = create_custom_level(layout)

    gr_obs = render_initial_board(brd, score)

    while not done(brd):
        move = read_player_input(brd, gr_obs)
        brd = update_board(brd, move, gr_obs)
        score += 1
        gr_obs['score'].setText(score)
        gr_obs['warning'].setText('')

    gr_obs['warning'].setText('You won in only {} moves! Press any key to quit.'.format(score))
    gr_obs['win'].getKey()
    time.sleep(.5)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()



# TODO
# Move graphics init to create_custom_level
# Pass around cars and use move() to move