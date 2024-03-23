""" 
--⪢ Main file responsible for handling user input and display current GameState.
"""

# import required libraries
import random
from math import inf

# score of capturing each piece
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
# global variables
CHECKMATE = inf
STALEMATE = 0
DEPTH = 3

# hashtable of scores of each board tile position for knights
knight_scores = [[0.0,  0.1,    0.2,    0.2,    0.2,    0.2,    0.1,    0.0],
                 [0.1,  0.3,    0.5,    0.5,    0.5,    0.5,    0.3,    0.1],
                 [0.2,  0.5,    0.6,    0.65,   0.65,   0.6,    0.5,    0.2],
                 [0.2,  0.55,   0.65,   0.7,    0.7,    0.65,   0.55,   0.2],
                 [0.2,  0.5,    0.65,   0.7,    0.7,    0.65,   0.5,    0.2],
                 [0.2,  0.55,   0.6,    0.65,   0.65,   0.6,    0.55,   0.2],
                 [0.1,  0.3,    0.5,    0.55,   0.55,   0.5,    0.3,    0.1],
                 [0.0,  0.1,    0.2,    0.2,    0.2,    0.2,    0.1,    0.0]]

# hashtable of scores of each board tile position for bishops
bishop_scores = [[0.0,  0.2,    0.2,    0.2,    0.2,    0.2,    0.2,    0.0],
                 [0.2,  0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.2],
                 [0.2,  0.4,    0.5,    0.6,    0.6,    0.5,    0.4,    0.2],
                 [0.2,  0.5,    0.5,    0.6,    0.6,    0.5,    0.5,    0.2],
                 [0.2,  0.4,    0.6,    0.6,    0.6,    0.6,    0.4,    0.2],
                 [0.2,  0.6,    0.6,    0.6,    0.6,    0.6,    0.6,    0.2],
                 [0.2,  0.5,    0.4,    0.4,    0.4,    0.4,    0.5,    0.2],
                 [0.0,  0.2,    0.2,    0.2,    0.2,    0.2,    0.2,    0.0]]

# hashtable of scores of each board tile position for rooks
rook_scores = [[0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.25],
               [0.5,    0.75,   0.75,   0.75,   0.75,   0.75,   0.75,   0.5],
               [0.0,    0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.0],
               [0.0,    0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.0],
               [0.0,    0.25,   0.25,   0.25,  0.25,   0.25,   0.25,   0.0],
               [0.0,    0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.0],
               [0.0,    0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.0],
               [0.25,   0.25,   0.25,   0.5,    0.5,    0.25,   0.25,   0.25]]

# hashtable of scores of each board tile position for queens
queen_scores = [[0.0,   0.2,    0.2,    0.3,    0.3,    0.2,    0.2,    0.0],
                [0.2,   0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.2],
                [0.2,   0.4,    0.5,    0.5,    0.5,    0.5,    0.4,    0.2],
                [0.3,   0.4,    0.5,    0.5,    0.5,    0.5,    0.4,    0.3],
                [0.4,   0.4,    0.5,    0.5,    0.5,    0.5,    0.4,    0.3],
                [0.2,   0.5,    0.5,    0.5,    0.5,    0.5,    0.4,    0.2],
                [0.2,   0.4,    0.5,    0.4,    0.4,    0.4,    0.4,    0.2],
                [0.0,   0.2,    0.2,    0.3,    0.3,    0.2,    0.2,    0.0]]

# hashtable of scores of each board tile position for pawns
pawn_scores = [[0.8,    0.8,    0.8,    0.8,    0.8,    0.8,    0.8,    0.8],
               [0.7,    0.7,    0.7,    0.7,    0.7,    0.7,    0.7,    0.7],
               [0.3,    0.3,    0.4,    0.5,    0.5,    0.4,    0.3,    0.3],
               [0.25,   0.25,   0.3,    0.45,   0.45,   0.3,    0.25,   0.25],
               [0.2,    0.2,    0.2,    0.4,    0.4,    0.2,    0.2,    0.2],
               [0.25,   0.15,   0.1,    0.2,    0.2,    0.1,    0.15,   0.25],
               [0.25,   0.3,    0.3,    0.0,    0.0,    0.3,    0.3,    0.25],
               [0.2,    0.2,    0.2,    0.2,    0.2,    0.2,    0.2,    0.2]]

# dictionary of piece types to their corresponding scores based on colors
piece_position_scores = {"wN": knight_scores, "bN": knight_scores[::-1],
                         "wB": bishop_scores, "bB": bishop_scores[::-1],
                         "wQ": queen_scores,  "bQ": queen_scores[::-1],
                         "wR": rook_scores,   "bR": rook_scores[::-1],
                         "wP": pawn_scores,   "bP": pawn_scores[::-1]}



def score_board(game_state):
    """ Function to find the score of a board form the given game state. A positive score indicates a white player's advantage. A negative score indicates a black player's advantage. """
    
    # check for endgame
    if game_state.check_mate:
        return -CHECKMATE if game_state.white_to_move else CHECKMATE                  # win condition reached
    
    # check for stalemate
    elif game_state.stale_mate:
        return STALEMATE

    score = 0

    # iterate through all rows on the game board
    for row, pieces in enumerate(game_state.board):
        # iterate through all pieces on the current row                            
        for col, piece in enumerate(pieces):  
            # if the piece is empty, skip it
            if piece == "--": continue
            
            # get the piece's score based on it's position, 0 if the pieces is king
            piece_position_score = 0 if piece[1] == "K" else piece_position_scores[piece][row][col]             # add heuristic based on piece position

            # add the piece's score to the total score based on it's color
            if piece[0] == "w":
                score += piece_score[piece[1]] + piece_position_score
            elif piece[0] == "b":
                score -= piece_score[piece[1]] + piece_position_score

    return score



def find_random_move(valid_moves):
    """ Picks and returns a random valid move. """
    
    return random.choice(valid_moves)
 



def find_best_move(game_state, valid_moves, return_queue):
    """  Helper method to make the first recursive call based on the min max algorithm """
    
    global next_move
    
    # initialize the next move as None, and shuffel the valid moves
    next_move = None
    random.shuffle(valid_moves)

    # find_move_min_max(game_state, valid_moves, DEPTH, game_state.white_to_move)                                             # only min max implementation
    find_move_min_max_alpha_beta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, game_state.white_to_move)           # min max with alpha beta pruning

    # return the next move from the global variable
    return_queue.put(next_move)




def find_move_min_max(game_state, valid_moves, depth, white_to_move):
    """ The best move based on min max algorithm alone """
    
    global next_move
    
    # base case to stop infinite recursion
    if depth == 0: return score_board(game_state)

    # if white to move, find the best move for white
    if white_to_move:

        # initialize the best score the maximum possible score
        max_score = -CHECKMATE
        for move in valid_moves:
            # make the move
            game_state.make_move(move)
            # get all the valid moves for the next player
            next_moves = game_state.get_all_valid_moves()
            # perform min max on the next player
            score = find_move_min_max(game_state, next_moves, depth-1, False)

            # if the score is better than the best score
            if score > max_score:
                max_score = score
                # if depth is the max depth, save the move
                if depth == DEPTH:
                    next_move = move

            # undo the last move
            game_state.undo_move()

        # return the best score
        return max_score

    # else, find the best move for black
    else:

        # initialize the best score the minium possible score
        min_score = CHECKMATE
        for move in valid_moves:
            # make the move
            game_state.make_move(move)
            # get all the valid moves for the next player
            next_moves = game_state.get_all_valid_moves()
            # perform min max on the next player
            score = find_move_min_max(game_state, next_moves, depth-1, True)

            # if the score is better than the best score
            if score < min_score:
                min_score = score
                # if depth is the max depth, save the move
                if depth == DEPTH:
                    next_move = move

            # undo the last move
            game_state.undo_move()

        # return the best score    
        return min_score
 


def find_move_min_max_alpha_beta(game_state, valid_moves, depth, alpha, beta, white_to_move):
    """ The best move based on min max algorithm with alpha beta pruning """
    
    global next_move
    
    # base case to stop infinite recursion
    if depth == 0: return score_board(game_state)                   

    # if white to move, find the best move for white
    if white_to_move:
        
        # initialize the best score the maximum possible score
        max_score = -CHECKMATE
        for move in valid_moves:
            # make the move
            game_state.make_move(move)
            # get all the valid moves for the next player
            next_moves = game_state.get_all_valid_moves()
            # perform min max on the next player
            cur_score = find_move_min_max_alpha_beta(game_state, next_moves, depth-1, alpha, beta, False)
            
            # if the score is better than the best score, update the best score
            if cur_score > max_score:
                max_score = cur_score
                # if depth is the max depth, save the move
                if depth == DEPTH:
                    next_move = move
            
            # undo the last move
            game_state.undo_move()

            # update alpha, if the alpha is higher or equal to beta, prune the branch
            alpha = max(alpha, max_score)
            if beta <= alpha:
                break

        return max_score

    else:
        # initialize the best score the minium possible score
        min_score = CHECKMATE
        for move in valid_moves:
            # make the move            
            game_state.make_move(move)
            # get all the valid moves for the next player
            next_moves = game_state.get_all_valid_moves()
            # perform min max on the next player
            cur_score = find_move_min_max_alpha_beta(game_state, next_moves, depth-1, alpha, beta, True)
            
            # if the score is better than the best score, update the best score
            if cur_score < min_score:
                min_score = cur_score
                # if depth is the max depth, save the move
                if depth == DEPTH:
                    next_move = move
            
            # undo the last move
            game_state.undo_move()

            # update beta, if the beta is lower or equal to alpha, prune the branch
            beta = min(beta, min_score)
            if beta <= alpha:
                break
    
        return min_score
