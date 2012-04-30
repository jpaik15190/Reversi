"""The engine to determine computer's best move."""

# CIS-192: Python Programming
# Spring 2012
# Final Project: Reversi
# Kristen Lau, Jay Paik, Paul Terwilliger
#
# Required modules: pygame, numpy
# Included module: textrect

import time
import array
import numpy as np

class BreakTreeSearch(Exception):
    """An exception created solely for breaking out of loops"""
    pass

class ReversiEngine(object):
    """Takes a given board and finds the best move through brute force
    by systematically trying every legal move.  
    Input is <board>, <current_turn>, and output is <move_chosen>"""
    
    def __init__(self, np_board, player):
        self.player = player
        self.player_f = ((self.player % 2) + 1)
        self.board = array.array("B", (np_board.flat))
        self.base_moves = []
        self.max_counter = 0

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

        self.corners = [0, 7, 56, 63]
        self.x_squares = [9, 14, 49, 54]

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

    def best(self, np_board):
        """Input is a <np.board>
        Create a tree of output boards and stops calculating after a time
       
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
        single = self.single
        m_app = self.base_moves.append
        turn = self.player
        turn_f = self.player_f
        curr = turn # curr stands for turn-current
        
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

        t_one_app = tree_one.append

        start = time.time()
        def stop(coor):
            """Use for calling BreakTreeSearch after 2.5 seconds"""
            elapsed = (time.time() - start)
            if elapsed > 2.5:
                raise BreakTreeSearch
            self.max_counter += 1
            return coor


        def first(brd):
            """Input is an array version of the board.
            Output is a list of all possible <output_boards> OR
            the original board in the case of no legal moves (passing)"""

            # Creates a list of legal and illegal output boards for every move
            gen = [single(brd, coor, curr) for coor in xrange(64) if (brd[
                                                                coor] == 0)]

            # Prunes out the illegal boards & uses the stop function on them.
            tree_num = [stop(out) for out in gen if (bool(out) == True)]

            if bool(tree_num) == False:
                return [brd[:]] # No possible moves
            return tree_num
        
        # Creates tree_one
        gen = [coor for coor in xrange(64) if (board[coor] == 0)]
        for coor in gen:
            out_brd = single(board, coor, turn)
            if bool(out_brd) == True:
                t_one_app(stop(out_brd))
                m_app(self.to_coors[coor]) # Remembers legal moves
        if bool(self.tree_one) == False:
            return # Pass

        def thr_lay(row_four):
            """Take the fourth row and returns the next level deep"""
            return [[map(first, row_two) for row_two in row_thr]
                                         for row_thr in row_four]

        def l_sev(row_seven):
            """Take the seventh row and returns the next level deep"""
            return [[map(thr_lay, row_fiv) for row_fiv in row_six]
                                           for row_six in row_seven]
        
        last_search = False # Remembers the tree that broke (BreakTreeSearch
        try: # Allows breaking out of loop with exception(BreakTreeSearch)
            while True:

                # Creates tree_two from the boards in tree_one
                if bool(tree_two) == False:
                    curr = turn_f
                    last_search = tree_two 
                    # "starting <tree_two>..."
                    tree_two = map(first, tree_one)
                    last_search = tree_thr

                # Creates tree_thr from the boards in tree_two
                elif bool(tree_thr) == False:
                    curr = turn
                    # "starting <tree_thr>..."
                    tree_thr = [map(first, row_two) for row_two in tree_two]
                    last_search = tree_fou

                # Creates tree_fou from the boards in tree_thr
                elif bool(tree_fou) == False:
                    curr = turn_f
                    # "starting <tree_fou>..."
                    tree_fou = thr_lay(tree_thr)
                    last_search = tree_fiv

                # Creates tree_fiv from the boards in tree_fou
                elif bool(tree_fiv) == False:
                    curr = turn
                    # "starting <tree_fiv>..."
                    tree_fiv = map(thr_lay, tree_fou)
                    last_search = tree_six

                # Creates tree_six from the boards in tree_fiv
                elif bool(tree_six) == False:
                    curr = turn_f
                    # "starting <tree_six>..."
                    tree_six = [map(thr_lay, row_fiv) for row_fiv in tree_fiv]
                    last_search = tree_sev

                # Creates tree_sev from the boards in tree_six
                elif bool(tree_sev) == False:
                    curr = turn
                    last_search = tree_sev
                    # "starting <tree_sev>..."
                    tree_sev = l_sev(tree_six)
                    last_search = tree_eig

                    raise BreakTreeSearch
                # Creates tree_eig from the boards in tree_sev
                elif bool(tree_eig) == False:
                    curr = turn_f
                    # "starting <tree_eig>..."
                    tree_eig = map(l_sev, tree_sev)
                    last_search = tree_nin

                # Creates tree_nin from the boards in tree_eig
                elif bool(tree_nin) == False:
                    curr = turn
                    # "starting <tree_nin>..."
                    tree_nin = [map(l_sev, row_eig) for row_eig in tree_eig]
                    last_search = False

                else:
                    last_search = False
                    break

        # BreakTreeSearch was raised
        except(BreakTreeSearch):
            pass
        
        final_eval = 0

        # For counting the score of tree_one
        if (bool(tree_nin) == True) and (tree_nin != last_search):
            final_eval = [min([max([min([max([min([max([min([max(
                                        map(self.c_score, row_two))
                                        for row_two in row_thr])
                                        for row_thr in row_fou])
                                        for row_fou in row_fiv])
                                        for row_fiv in row_six])
                                        for row_six in row_sev])
                                        for row_sev in row_eig])
                                        for row_eig in row_nin])
                                        for row_nin in tree_nin]

        # For counting the score of tree_one
        if (bool(tree_eig) == True) and (tree_eig != last_search):
            final_eval = [min([max([min([max([min([max([min(
                                        map(self.c_score, row_two))
                                        for row_two in row_thr])
                                        for row_thr in row_fou])
                                        for row_fou in row_fiv])
                                        for row_fiv in row_six])
                                        for row_six in row_sev])
                                        for row_sev in row_eig])
                                        for row_eig in tree_eig]

        # For counting the score of tree_one
        elif (bool(tree_sev) == True) and (tree_sev != last_search):
            final_eval = [min([max([min([max([min([max(
                                        map(self.c_score, row_two))
                                        for row_two in row_thr])
                                        for row_thr in row_fou])
                                        for row_fou in row_fiv])
                                        for row_fiv in row_six])
                                        for row_six in row_sev])
                                        for row_sev in tree_sev]

        # For counting the score of tree_one
        elif (bool(tree_six) == True) and (tree_six != last_search):
            final_eval = [min([max([min([max([min(map(self.c_score, row_two))
                                        for row_two in row_thr])
                                        for row_thr in row_fou])
                                        for row_fou in row_fiv])
                                        for row_fiv in row_six])
                                        for row_six in tree_six]

        # For counting the score of tree_one
        elif (bool(tree_fiv) == True) and (tree_fiv != last_search):
            final_eval = [min([max([min([max(map(self.c_score, row_two))
                                        for row_two in row_thr])
                                        for row_thr in row_fou])
                                        for row_fou in row_fiv])
                                        for row_fiv in tree_fiv]

        # For counting the score of tree_one
        elif (bool(tree_fou) == True) and (tree_fou != last_search):
            final_eval = [min([max([min(map(self.c_score, row_two))
                                        for row_two in row_thr])
                                        for row_thr in row_fou])
                                        for row_fou in tree_fou]

        # For counting the score of tree_one
        elif (bool(tree_thr) == True) and (tree_thr != last_search):
            final_eval = [min([max(map(self.c_score, row_two))
                                        for row_two in row_thr])
                                        for row_thr in tree_thr]

        # For counting the score of tree_one
        elif (bool(tree_two) == True) and (tree_two != last_search):
            final_eval = [min(map(self.c_score, row_two))
                                        for row_two in tree_two]

        # For counting the score of tree_one
        elif (bool(tree_one) == True) and (tree_one != last_search):
            final_eval = map(self.c_score, tree_one)
        
        final_coor = 0
        for (coor, val) in enumerate(final_eval):
            if val == max(final_eval):
                final_coor = coor
                break

        return self.base_moves[final_coor]
       
    def single(self, dont_touch_this_board, ar_move, turn):
        """Input is an <array>, <move_tuple>, <turn>.
        Output is either: <final_board> OR <same_board>"""
        
        def lgal(flip_list, turn):
            """Input is a list of <array_coors>, <turn>
            Output is a list of to-be-flipped pebbles list(<array_coors>)."""
            counter = 0
            sec = 0
            for num in flip_list:
                if board[num] == 0:
                    break
                elif board[num] == turn:
                    counter = sec
                    break
                sec += 1
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

        # Enemy north
        if (1 < coo_y) and (board[self.to_array[((coo_y - 1), coo_x
                                                        )]] == turn_f):
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
        if (coo_x < 6) and (board[self.to_array[(coo_y, (coo_x + 1)
                                                        )]] == turn_f):
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
        if (coo_y < 6) and (board[self.to_array[((coo_y + 1), coo_x
                                                        )]] == turn_f):
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
        if (1 < coo_x) and (board[self.to_array[(coo_y, (coo_x - 1)
                                                        )]] == turn_f):
            coors_y = [coo_y for num in xrange(8)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            west_ = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        # Enemy north-west
        if (1 < coo_y) and (1 < coo_x) and (board[
                    self.to_array[((coo_y - 1), (coo_x - 1))]] == turn_f):
            coors_y = [coor for coor in xrange(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in xrange(coo_x - 1, -1, -1)]
            nwest = [self.to_array[coo] for coo in zip(coors_y, coors_x)]
        
        flip = (lgal(north, turn) + lgal(neast, turn)
                         + lgal(east_, turn) + lgal(seast, turn)
                         + lgal(south, turn) + lgal(swest, turn)
                         + lgal(west_, turn) + lgal(nwest, turn))
        

        # Flips over the pebbles chosen by flip
        legal = False
        for ar_flipped in flip:
            if legal == False:
                legal = True
            board[ar_flipped] = turn
        if legal == True: # Implements the chosen turn
            board[ar_move] = turn
            return board
        elif legal == False:
            return False # Not a legal move, don't return a board
        
    def c_score(self, board):
        """Count the current score.  
        Input is a <array>, output is the <score> of the board.
        For every player pebble: <score> += 1;
        For every enemy pebble: <score> -= 1"""
        score = board.count(1) - board.count(2)
        for x_square in self.x_squares:
            if board[x_square] == 1:
                score -= 2
            elif board[x_square] == 2:
                score += 2
        for corner in self.corners:
            if board[corner] == 1:
                score += 8
            elif board[corner] == 2:
                score -= 8
        if self.player == 2:
            score = (-1) * score
        return score

