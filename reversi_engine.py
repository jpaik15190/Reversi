"""CIS192 Final Project; reversi_engine.py; Paul Terwilliger, Jay Paik, Kirsten Lau

Ideas to consider:
-bitboards
-numpy, array
-pypy
http://www.squidoo.com/freelancedeveloper
"""

import copy

class Reversi_Engine(object):
    """Takes a given board and finds the best move by systematically trying every legal move.  
    Input is <board>, <current_turn>, and output is <move_chosen>"""
    
    def __init__(self, board, turn):
        self.board = board
        turn = turn
        self.base_moves = []
        
        # Sets of moves in a tree
        self.tree_one = []
        self.tree_two = []
        self.tree_thr = []
        self.tree_fou = []
        self.tree_fiv = []
        self.tree_six = []
        self.tree_sev = []
        self.tree_eig = []
        self.tree_nin = []
        self.tree_ten = []
        
    def main_func(self, board, turn):
        """Creates a tree of output boards with a max calculation of <max_counter>
board    = %

tree_one =  [%, %, %]

tree_two = [[%, %, %], [%, %, %], [%, %, %]]

tree_thr = [[[%, %, %], [%, %, %], [%, %, %]],
            [[%, %, %], [%, %, %], [%, %, %]],
            [[%, %, %], [%, %, %], [%, %, %]]],

tree_fou = [[[[%, %, %], [%, %, %], [%, %, %]],
             [[%, %, %], [%, %, %], [%, %, %]],
             [[%, %, %], [%, %, %], [%, %, %]]],

            [[[%, %, %], [%, %, %], [%, %, %]],
             [[%, %, %], [%, %, %], [%, %, %]],
             [[%, %, %], [%, %, %], [%, %, %]]],

            [[[%, %, %], [%, %, %], [%, %, %]],
             [[%, %, %], [%, %, %], [%, %, %]],
             [[%, %, %], [%, %, %], [%, %, %]]]]

...
        """
        
        print_ = self.print_
        all_zeros = self.all_zeros
        single_move = self.single_move
        keep_going = True
        max_counter = 400
        m_app = self.base_moves.append
        
        tree_one = self.tree_one
        tree_two = self.tree_two
        tree_thr = self.tree_thr
        tree_fou = self.tree_fou
        tree_fiv = self.tree_fiv
        tree_six = self.tree_six
        tree_sev = self.tree_sev
        tree_eig = self.tree_eig
        
        t_one_app = tree_one.append
        t_two_app = tree_two.append
        t_thr_app = tree_thr.append
        t_fou_app = tree_fou.append
        t_fiv_app = tree_fiv.append
        t_six_app = tree_six.append
        t_sev_app = tree_sev.append
        t_eig_app = tree_eig.append

        #run function to make board lighter?
        
        # Make the list of first-tier <tree_one> boards and the possible moves
        def first_app(boar, max_counter, turn):
            """Input is a <board> (with the proper appending and zeroing powers)
            Output is <out_board>s OR False"""
            tree_num = []
            t_app = tree_num.append
            zeros = all_zeros(boar)
            if bool(zeros) == True:
                for (num, ber) in zeros:
                #for x in range(1):
                    out_board = single_move(boar, (num, ber), turn)
                    if bool(out_board) == True:
                        max_counter -= 1
                        t_app((out_board))
                        #t_app([[1]])
                return (max_counter, tree_num)
            elif bool(zeros) == False:
                return False # No possible moves???  Needs editing (a response)
        
        zeros = all_zeros(board)
        if bool(zeros) == True:
            for (num, ber) in zeros:
                out_board = single_move(board, (num, ber), turn)
                if bool(out_board) == True:
                    max_counter -= 1
                    t_one_app(out_board)
                    m_app((num, ber))
        elif bool(zeros) == False:
            pass # No possible moves???  Needs editing (a response)
        
        # Test to see if the original board is affected
        #for boar in tree_one:
            #print_(boar)
        #print_(board)
        #print self.base_moves
        
        
        while keep_going == True:
            if max_counter == 0:
                keep_going == False
                print "max_counter == 0"
                break
            elif bool(tree_two) == False:
                print "hi"
                for boar in tree_one:
                    
                    test_x = first_app(boar, max_counter, ((turn % 2) + 1))
                    t_two_app(test_x[1])
                    max_counter = test_x[0]
                    print tree_two
                    print max_counter
            elif bool(tree_thr) == False:
                print "three"
                tree_thr = [[]]
                for row_first in tree_two:
                    test_y = []
                    t_y_app = test_y.append
                    for boar in row_first:
                        print boar
                        test_x = first_app(boar, max_counter, turn)
                        t_y_app(test_x[1])
                        max_counter = test_x[0]
                        print max_counter
                    print ">>>>", test_y
                    tree_thr.append(test_y)
                    print "------>", tree_thr
                    print max_counter
            else:
                max_counter -= 1
                #figure out all boards
                #check <max_counter>
                #turn all moves into <tree_two> when all are completed
            #....
        #count all tiles in highest tree_###
        #do that tree
        #after doing that tree, keep old trees?
        
    def single_move(self, dont_touch_this_board, coor_move, turn):
        """Input is a board, selected move (in a tuple), and current turn.
        Output is either: <final_board> OR False"""
        
        def legal(flip_list, turn):
            """Input is a list of two-integer tuples which are coordinates,
            output is a list with the to-be-flipped pebbles remaining."""
            legal = False
            counter = 0
            for (num, ber) in flip_list:
                if board[num][ber] == ((turn % 2) + 1):
                    counter += 1
                elif board[num][ber] == 0:
                    counter = 0
                    break
                elif board[num][ber] == turn:
                    legal = True
                    break
            if legal == False:
                counter = 0
            return flip_list[:counter]

        # Defined variables:
        board = copy.deepcopy(dont_touch_this_board)
        coo_y = coor_move[0]
        coo_x = coor_move[1]
        turn_f = ((turn % 2) + 1)
        flip = []
        north = []
        neast = []
        east_ = []
        seast = []
        south = []
        swest = []
        west_ = []
        nwest = []

        # Enemy north
        if (1 < coo_y) and (board[coo_y - 1][coo_x] == turn_f):
            coors_y = [coor for coor in xrange(coo_y - 1, -1, -1)]
            coors_x = [coo_x for num in xrange(8)]
            north = zip(coors_y, coors_x)
            
        # Enemy north-east
        if (1 < coo_y) and (coo_x < 6) and (board[coo_y - 1][coo_x + 1] == turn_f):
            coors_y = [coor for coor in xrange(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in xrange(coo_x + 1, 8)]
            neast = zip(coors_y, coors_x)
        
        # Enemy east
        if (coo_x < 6) and (board[coo_y][coo_x + 1] == turn_f):
            coors_y = [coo_y for num in xrange(8)]
            coors_x = [coor for coor in xrange(coo_x + 1, 8)]
            east_ = zip(coors_y, coors_x)
        
        # Enemy south-east        
        if (coo_y < 6) and (coo_x < 6) and (board[coo_y + 1][coo_x + 1] == turn_f):
            coors_y = [coor for coor in xrange(coo_y + 1, 8)]
            coors_x = [coor for coor in xrange(coo_x + 1, 8)]
            seast = zip(coors_y, coors_x)
            
        # Enemy south
        if (coo_y < 6) and (board[coo_y + 1][coo_x] == turn_f):
            coors_y = [coor for coor in xrange(coo_y + 1, 8)]
            coors_x = [coo_x for num in xrange(8)]
            south = zip(coors_y, coors_x)
        
        # Enemy south-west
        if (coo_y < 6) and (1 < coo_x) and (board[coo_y + 1][coo_x - 1] == turn_f):
            coors_y = [coor for coor in xrange(coo_y + 1, 8)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            swest = zip(coors_y, coors_x)
        
        #Enemy west
        if (1 < coo_x) and (board[coo_y][coo_x - 1] == turn_f):
            coors_y = [coo_y for num in xrange(8)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            west_ = zip(coors_y, coors_x)
        
        # Enemy north-west
        if (1 < coo_y) and (1 < coo_x) and (board[coo_y - 1][coo_x - 1] == turn_f):
            coors_y = [coor for coor in xrange(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            nwest = zip(coors_y, coors_x)
        
        flip = (legal(north, turn) + legal(neast, turn) + legal(east_, turn) + legal(seast, turn)
              + legal(south, turn) + legal(swest, turn) + legal(west_, turn) + legal(nwest, turn))
        
        # Flips over the pebbles chosen by flip
        lgal = False
        for (num, ber) in flip:
            if lgal == False:
                lgal = True
            board[num][ber] = turn
        if lgal == True:
            board[coo_y][coo_x] = turn
            return board
        elif lgal == False:
            return False
        
    def all_zeros(self, board):
        """Input is a board, output is every empty tile in the board <list_of_tuples>"""
        num = -1
        available = []
        aval_app = available.append
        for row in board:
            num += 1
            ber = 0
            for square in row:
                if square == 0:
                    aval_app((num, ber))
                ber += 1
        return available
    
    def count_score(self, board, turn):
        """Counts the current score.  Input is a <board>, output is the <score> of the board.
        For every player pebble: <score> += 1; For every enemy pebble: <score> -= 1"""
        score = 0
        for row in board:
            for square in row:
                if square == 1:
                    score += 1
                elif square == 2:
                    score -= 1
        if turn == 2:
            score = (-1) * score
        return score
    
    def print_(self, board):
        """Prints the board: temporary function for developing code"""
        print "{})0  1  2  3  4  5  6  7 ".format("00")
        col_num = 0
        for row in board:
            print "{} {}".format(col_num, row)
            col_num += 1
        print "--------------------------"


board = [[0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 0, 0, 1, 2, 0, 0, 0,],
         [0, 0, 0, 2, 1, 0, 0, 0,],
         [0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 0, 0, 0, 0, 0, 0, 0,]]

revers = Reversi_Engine(board, 1)
revers.main_func(board, 1)