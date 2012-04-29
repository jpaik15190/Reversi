"""CIS192 Final Project; reversi_engine.py; Paul Terwilliger, Jay Paik, Kirsten Lau"""

import time
import array
import numpy as np

class BreakTreeSearch(Exception):
    """An exception created solely for breaking out of loops"""
    pass

class ReversiEngine(object):
    """Takes a given board and finds the best move by systematically trying every legal move.  
    Input is <board>, <current_turn>, and output is <move_chosen>"""
    
    def __init__(self, np_board, turn):
        self.turn = turn
        self.turn_f = ((self.turn % 2) + 1)
        self.board = array.array("B", (np_board.flat))
        self.base_moves = []
        self.max_counter = 0

        self.elapsed = 0     # Temporary for developing code
        self.elapsed_two = 0 # Temporary for developing code
        
        self.to_array = { # For converting <tuple_coors> to <array_coors>
            (0, 0):  0, (0, 1):  1, (0, 2):  2, (0, 3):  3, (0, 4):  4, 
                                    (0, 5):  5, (0, 6):  6, (0, 7):  7,
            (1, 0):  8, (1, 1):  9, (1, 2): 10, (1, 3): 11, (1, 4): 12, 
                                    (1, 5): 13, (1, 6): 14, (1, 7): 15,
            (2, 0): 16, (2, 1): 17, (2, 2): 18, (2, 3): 19, (2, 4): 20, 
                                    (2, 5): 21, (2, 6): 22, (2, 7): 23,
            (3, 0): 24, (3, 1): 25, (3, 2): 26, (3, 3): 27, (3, 4): 28, 
                                    (3, 5): 29, (3, 6): 30, (3, 7): 31,
            (4, 0): 32, (4, 1): 33, (4, 2): 34, (4, 3): 35, (4, 4): 36, 
                                    (4, 5): 37, (4, 6): 38, (4, 7): 39,
            (5, 0): 40, (5, 1): 41, (5, 2): 42, (5, 3): 43, (5, 4): 44, 
                                    (5, 5): 45, (5, 6): 46, (5, 7): 47,
            (6, 0): 48, (6, 1): 49, (6, 2): 50, (6, 3): 51, (6, 4): 52, 
                                    (6, 5): 53, (6, 6): 54, (6, 7): 55,
            (7, 0): 56, (7, 1): 57, (7, 2): 58, (7, 3): 59, (7, 4): 60, 
                                    (7, 5): 61, (7, 6): 62, (7, 7): 63}

        self.to_coors = { # For converting <array_coors> to <tuple_coors>
             0: (0, 0),  1: (0, 1),  2: (0, 2),  3: (0, 3),  4: (0, 4),
                                     5: (0, 5),  6: (0, 6),  7: (0, 7),
             8: (1, 0),  9: (1, 1), 10: (1, 2), 11: (1, 3), 12: (1, 4),
                                    13: (1, 5), 14: (1, 6), 15: (1, 7),
            16: (2, 0), 17: (2, 1), 18: (2, 2), 19: (2, 3), 20: (2, 4),
                                    21: (2, 5), 22: (2, 6), 23: (2, 7),
            24: (3, 0), 25: (3, 1), 26: (3, 2), 27: (3, 3), 28: (3, 4),
                                    29: (3, 5), 30: (3, 6), 31: (3, 7),
            32: (4, 0), 33: (4, 1), 34: (4, 2), 35: (4, 3), 36: (4, 4),
                                    37: (4, 5), 38: (4, 6), 39: (4, 7),
            40: (5, 0), 41: (5, 1), 42: (5, 2), 43: (5, 3), 44: (5, 4),
                                    45: (5, 5), 46: (5, 6), 47: (5, 7),
            48: (6, 0), 49: (6, 1), 50: (6, 2), 51: (6, 3), 52: (6, 4),
                                    53: (6, 5), 54: (6, 6), 55: (6, 7),
            56: (7, 0), 57: (7, 1), 58: (7, 2), 59: (7, 3), 60: (7, 4),
                                    61: (7, 5), 62: (7, 6), 63: (7, 7)} 

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
        self.tree_ele = []
        self.tree_twe = []
            

    def best(self, np_board):
        """Input is a <np.board>
        Creates a tree of output boards and stops calculating after a time
       
        board    = %

        tree_one =    [%, %, %]

        tree_two =   [[%, %, %], [%, %, %], [%, %, %]]

        tree_thr =  [[[%, %, %], [%, %, %], [%, %, %]],
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
        """

        self.base_moves = []
        board = array.array("B", (np_board.flat))
        single_move = self.single_move
        m_app = self.base_moves.append
        turn = self.turn
        turn_f = self.turn_f
        turn_c = turn
        
        # Designating variables for the trees
        tree_one = self.tree_one = []
        tree_two = self.tree_two = []
        tree_thr = self.tree_thr = []
        tree_fou = self.tree_fou = []
        tree_fiv = self.tree_fiv = []
        tree_six = self.tree_six = []
        tree_sev = self.tree_sev = []
        tree_eig = self.tree_eig = []
        tree_nin = self.tree_nin = []
        tree_ten = self.tree_ten = []
        tree_ele = self.tree_ele = []
        tree_twe = self.tree_twe = []

        t_one_app = tree_one.append
        t_two_app = tree_two.append
        t_thr_app = tree_thr.append
        t_fou_app = tree_fou.append
        t_fiv_app = tree_fiv.append
        t_six_app = tree_six.append
        t_sev_app = tree_sev.append
        t_eig_app = tree_eig.append
        t_nin_app = tree_nin.append
        t_ten_app = tree_ten.append
        t_ele_app = tree_ele.append
        t_twe_app = tree_twe.append

        start = time.time()
        def counting(coor):
            """Used for calling BreakTreeSearch"""
            elapsed = (time.time() - start)
            if elapsed > 1:
                raise BreakTreeSearch
            self.max_counter += 1
            return coor


        def first_app(brd):
            """Input is an <array>; Output is all possible <output_boards> OR the original
            board in the case of no legal moves (passing)"""

            # Creates a list of output boards for every move, both legal and illegal
            b_gen = [single_move(brd, coor, turn_c) for coor in xrange(64) if brd[coor] == 0]

            # Prunes out the illegal boards and uses the counting function on them.
            tree_num = [counting(out_brd) for out_brd in b_gen if (bool(out_brd) == True)]
            if bool(tree_num) == False:
                return [brd[:]] # No possible moves? Needs editing (a response) NEEDS WEIGHIING
            return tree_num
        
        # Creates tree_one
        b_gen = [coor for coor in xrange(64) if (board[coor] == 0)]
        for coor in b_gen:
            out_brd = single_move(board, coor, turn)
            if bool(out_brd) == True:
                t_one_app(counting(out_brd))
                m_app(self.to_coors[coor])

        current_search = False
        try: # Allows me to break out of the loop with the exception BreakTreeSearch
            while True:
                
                # Creates tree_two from the boards in tree_one
                if bool(tree_two) == False:
                    turn_c = turn_f
                    current_search = tree_two 
                    print "starting <tree_two>..."
                    tree_two = map(first_app, tree_one)

                # Creates tree_thr from the boards in tree_two
                elif bool(tree_thr) == False:
                    turn_c = turn
                    current_search = tree_thr
                    print "starting <tree_thr>..."
                    tree_thr = [map(first_app, row_two) for row_two in tree_two]
                    current_search = tree_fou
                    raise BreakTreeSearch

                # Creates tree_fou from the boards in tree_thr
                elif bool(tree_fou) == False:
                    turn_c = turn_f
                    current_search = tree_fou
                    print "starting <tree_fou>..."
                    for row_thr in tree_thr:
                        row_fou = [map(first_app, row_two) for row_two in row_thr]
                        t_fou_app(row_fou)
                    print "4: <max_counter> =", self.max_counter
                elif bool(tree_fiv) == False:
                    turn_c = turn
                    current_search = tree_fiv
                    print "starting <tree_fiv>..."
                    for row_fou in tree_fou:
                        row_fiv = [[map(first_app, row_two) for row_two in row_thr]
                                                            for row_thr in row_fou]
                        t_fiv_app(row_fiv)
                    print "5: <max_counter> =", self.max_counter
                elif bool(tree_six) == False:
                    turn_c = turn_f
                    current_search = tree_six
                    print "starting <tree_six>..."
                    for row_fiv in tree_fiv:
                        tmp_six = []
                        tmp_six_app = tmp_six.append
                        for row_fou in row_fiv:
                            tmp_fiv = []
                            tmp_fiv_app = tmp_fiv.append
                            for row_thr in row_fou:
                                tmp_fou = [[first_app(board_f) for board_f in row_two]
                                                               for row_two in row_thr]
                                tmp_fiv_app(tmp_fou)
                            tmp_six_app(tmp_fiv)
                        t_six_app(tmp_six)
                    print "6: <max_counter> =", self.max_counter
                elif bool(tree_sev) == False:
                    turn_c = turn
                    current_search = tree_sev
                    print "starting <tree_sev>..."
                    for row_six in tree_six:
                        tmp_sev = []
                        tmp_sev_app = tmp_sev.append
                        for row_fiv in row_six:
                            tmp_six = []
                            tmp_six_app = tmp_six.append
                            for row_fou in row_fiv:
                                tmp_fiv = []
                                tmp_fiv_app = tmp_fiv.append
                                for row_thr in row_fou:
                                    tmp_fou = [map(first_app, row_two) for row_two in row_thr]
                                    tmp_fiv_app(tmp_fou)
                                tmp_six_app(tmp_fiv)
                            tmp_sev_app(tmp_six)
                        t_sev_app(tmp_sev)
                    print "7: <max_counter> =", self.max_counter
                else:
                    current_search = False
                    break
        except(BreakTreeSearch):
            pass
        
        final_eval = 0
        if (bool(tree_eig) == True) and (tree_eig != current_search):
            pass
        elif (bool(tree_sev) == True) and (tree_sev != current_search):
            res_sev = []
            for row_sev in tree_sev:
                res_six = []
                for row_six in tree_six:
                    res_fiv = []
                    for row_fiv in tree_fiv:
                        res_fou = []
                        for row_fou in tree_fou:
                            res_thr = []
                            for row_thr in tree_thr:
                                res_two = []
                                for row_two in row_thr:
                                    res_one = [self.c_score(brd) for brd in row_two]
                                    res_two.append(max(res_one))
                                res_thr.append(min(res_two))
                            res_fou.append(max(res_thr))
                        res_fiv.append(min(res_fou))
                    res_six.append(max(res_fiv))
                res_sev.append(min(res_six))
            print "res_sev:", res_sev
            final_eval = res_sev
 

        elif (bool(tree_six) == True) and (tree_six != current_search):
            res_six = []
            for row_six in tree_six:
                res_fiv = []
                for row_fiv in tree_fiv:
                    res_fou = []
                    for row_fou in tree_fou:
                        res_thr = []
                        for row_thr in tree_thr:
                            res_two = []
                            for row_two in row_thr:
                                res_one = [self.c_score(brd) for brd in row_two]
                                res_two.append(min(res_one))
                            res_thr.append(max(res_two))
                        res_fou.append(min(res_thr))
                    res_fiv.append(max(res_fou))
                res_six.append(min(res_fiv))
            print "res_six:", res_six
            final_eval = res_six
 
        elif (bool(tree_fiv) == True) and (tree_fiv != current_search):
            res_fiv = []
            for row_fiv in tree_fiv:
                res_fou = []
                for row_fou in tree_fou:
                    res_thr = []
                    for row_thr in tree_thr:
                        res_two = []
                        for row_two in row_thr:
                            res_one = [self.c_score(brd) for brd in row_two]
                            res_two.append(max(res_one))
                        res_thr.append(min(res_two))
                    res_fou.append(max(res_thr))
                res_fiv.append(min(res_fou))
            print "res_fiv:", res_fiv
            final_eval = res_fiv
        elif (bool(tree_fou) == True) and (tree_fou != current_search):
            res_fou = []
            for row_fou in tree_fou:
                res_thr = []
                for row_thr in tree_thr:
                    res_two = []
                    for row_two in row_thr:
                        res_one = map(self.c_score, row_two)
                        res_two.append(min(res_one))
                    res_thr.append(max(res_two))
                res_fou.append(min(res_thr))
            print "res_fou:", res_fou
            final_eval = res_fou
        elif (bool(tree_thr) == True) and (tree_thr != current_search):
            res_thr = []
            for row_thr in tree_thr:
                res_two = []
                for row_two in row_thr:
                    res_one = map(self.c_score, row_two)
                    res_two.append(max(res_one))
                res_thr.append(min(res_two))
            print "res_thr:", res_thr
            final_eval = res_thr
        elif (bool(tree_two) == True) and (tree_two != current_search):
            res_two = []
            for row_two in tree_two:
                res_one = map(self.c_score, row_two)
                res_two.append(min(res_one))
            print "res_two:", res_two 
            final_eval = res_two
        elif (bool(tree_one) == True) and (tree_one != current_search):
            res_one = map(self.c_score, tree_one)
            print "res_one:", res_one
            final_eval = res_one
        
        final_coor = 0
        for (coor, val) in enumerate(final_eval):
            if val == max(final_eval):
                final_coor = coor
                break
       
        print self.elapsed, "<-- ELAPSED"
        print self.base_moves[final_coor]
        return self.base_moves[final_coor]
       
    def single_move(self, dont_touch_this_board, ar_move, turn):
        """Input is an <array>, <move_tuple>, <turn>.
        Output is either: <final_board> OR <same_board>"""
        
        def lgal(flip_list, turn):
            """Input is a list of <array_coors>, <turn>
            Output is a list of the to-be-flipped pebbles list(<array_coors>)."""
            #startt = time.time()
            counter = 0
            sec = 0
            for num in flip_list:
                if board[num] == 0:
                    break
                elif board[num] == turn:
                    counter = sec
                    break
                sec += 1
            #self.elapsed_two += time.time() - startt
            return flip_list[:counter]

        # Defined variables:
        board = dont_touch_this_board[:]
        coor_move = self.to_coors[ar_move]
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

        start = time.time()

        # Enemy north
        if (1 < coo_y) and (board[self.to_array[((coo_y - 1), coo_x)]] == turn_f):
            coors_y = [coor for coor in xrange(coo_y - 1, -1, -1)]
            coors_x = [coo_x for num in xrange(8)]
            north = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
            
        # Enemy north-east
        if (1 < coo_y) and (coo_x < 6) and (board[
                                self.to_array[((coo_y - 1), (coo_x + 1))]] == turn_f):
            coors_y = [coor for coor in xrange(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in xrange(coo_x + 1, 8)]
            neast = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        # Enemy east
        if (coo_x < 6) and (board[self.to_array[(coo_y, (coo_x + 1))]] == turn_f):
            coors_y = [coo_y for num in xrange(8)]
            coors_x = [coor for coor in xrange(coo_x + 1, 8)]
            east_ = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        # Enemy south-east        
        if (coo_y < 6) and (coo_x < 6) and (board[
                                self.to_array[((coo_y + 1), (coo_x + 1))]] == turn_f):
            coors_y = [coor for coor in xrange(coo_y + 1, 8)]
            coors_x = [coor for coor in xrange(coo_x + 1, 8)]
            seast = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
            
        # Enemy south
        if (coo_y < 6) and (board[self.to_array[((coo_y + 1), coo_x)]] == turn_f):
            coors_y = [coor for coor in xrange(coo_y + 1, 8)]
            coors_x = [coo_x for num in xrange(8)]
            south = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        # Enemy south-west
        if (coo_y < 6) and (1 < coo_x) and (board[
                                self.to_array[((coo_y + 1), (coo_x - 1))]] == turn_f):
            coors_y = [coor for coor in xrange(coo_y + 1, 8)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            swest = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        #Enemy west
        if (1 < coo_x) and (board[self.to_array[(coo_y, (coo_x - 1))]] == turn_f):
            coors_y = [coo_y for num in xrange(8)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            west_ = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        # Enemy north-west
        if (1 < coo_y) and (1 < coo_x) and (board[
                                self.to_array[((coo_y - 1), (coo_x - 1))]] == turn_f):
            coors_y = [coor for coor in xrange(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            nwest = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        flip = (lgal(north, turn) + lgal(neast, turn) + lgal(east_, turn) + lgal(seast, turn)
              + lgal(south, turn) + lgal(swest, turn) + lgal(west_, turn) + lgal(nwest, turn))
        
        self.elapsed += time.time() - start

        # Flips over the pebbles chosen by flip
        legal = False
        for ar_flipped in flip:
            if legal == False:
                legal = True
            board[ar_flipped] = turn
        if legal == True: # Implements the chosen turn if at least one pebble is flipped
            board[ar_move] = turn
            return board
        elif legal == False:
            return False # Not a legal move, don't return a board
        
    def c_score(self, board):
        """Counts the current score.  Input is a <array>, output is the <score> of the board.
        For every player pebble: <score> += 1; For every enemy pebble: <score> -= 1"""
        try:
            score = board.count(1) - board.count(2)
            if self.turn == 2:
                score = (-1) * score
            return score
        except(AttributeError):
            print board, "<<< AttributeError!!!!!!!!"

'''
boary = [[0, 0, 0, 0, 0, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 0, 0, 0, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 0, 0, 0, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 0, 1, 2, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 0, 2, 1, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 0, 0, 0, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 0, 0, 0, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 0, 0, 0, 0, 0, 0,]]  # Temporary for developing code

board = [[0, 0, 0, 0, 0, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 2, 0, 0, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 2, 2, 1, 1, 2, 0,],  # Temporary for developing code
         [0, 0, 2, 1, 2, 1, 0, 0,],  # Temporary for developing code
         [0, 0, 2, 1, 1, 2, 2, 0,],  # Temporary for developing code
         [0, 0, 1, 0, 1, 1, 2, 0,],  # Temporary for developing code
         [0, 1, 2, 0, 2, 0, 0, 0,],  # Temporary for developing code
         [0, 0, 2, 0, 0, 0, 0, 0,]]  # Temporary for developing code


start = time.time()  # Temporary for developing code
boardnp = np.array(board)  # Temporary for developing code
board = array.array("B", boardnp.flat)  # Temporary for developing code
revers = ReversiEngine(boardnp, 1)  # Temporary for developing code
revers.best(boardnp)  # Temporary for developing code
elapsed = (time.time() - start)  # Temporary for developing code
print elapsed  # Temporary for developing code
print "<max_counter> =", revers.max_counter  # Temporary for developing code'''
