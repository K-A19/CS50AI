"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Initialises variables to keep track of the number of X's or O's on the board
    moves_x = 0
    moves_o = 0

    for row in board:
        for value in row:
            # Checks if that square contains an X
            if value == X:
                moves_x += 1

            # Checks if that square contains an O
            if value == O:
                moves_o += 1

            # If it is neither contains an X or O we can assume it is EMPTY

    # If there is an equal number of moves made by both X and O players, then it is player X's turn to play
    if moves_x == moves_o:
        return X

    # If they are not equal then it would be player O's turn to player as X always starts first
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Initialises a list which may be used to store the action tuples
    moves = []

    # Iterates over each row and then each cell per row
    for y in range(3):
        for z in range(3):
            if board[y][z] == EMPTY:
                moves.append((y, z))

    # Checks if the moves list is empty in order to return None
    if len(moves) < 1:
        return None

    # If the list isn't empty, the moves list is returnedwith all action tuples
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Creates a copy of the board
    dup = copy.deepcopy(board)

    # Checks to see if the action is actually valid
    try:
        # If action is valid, the board copy is altered in order contain new action
        dup[action[0]][action[1]] = player(board)

        # Return the newly updated board
        return dup

    except Exception:
        raise ValueError

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for i in range(3):
        # Checks if a player won horizontally
        if board[i][0] == board[i][1] == board[i][2] and board[i][1] != EMPTY:
            return board[i][0]

        # Checks if a player won vartically
        if board[0][i] == board[1][i] == board[2][i] and board[1][i] != EMPTY:
            return board[0][i]

    # Checks if the player won diagonally from top left to bottom right
    if board[0][0] == board[1][1] == board[2][2] and board[1][1] != EMPTY:
        return board[1][1]

    # Checks if the player won diagonally from bottom left to top right
    if board[2][0] == board[1][1] == board[0][2] and board[1][1] != EMPTY:
        return board[1][1]

    # Assumes the game is still in play or there was a tie and return None, since there are no invalid boards inputted
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Returns true if there is a winner in the current board
    if winner(board) != None:
        return True

    if actions(board) == None:
        return True

    # Returns false assuming the game is still in progress
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Gets the winner of the game or if there is a tie
    result = winner(board)

    # Returns 1 if the winner is X
    if result == X:
        return 1

    # Returns -1 if the winner is O
    elif result == O:
        return -1

    # Returns 0 if there is a draw as it is a terminal board and the game can no longer be in progress
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Makes sure the board is not in a terminal state already
    if terminal(board):
        return None

    # Returns the most optimal action as a max player, which is X, trying to maximize their score
    if player(board) == X:
        move = MAX_VALUE(board)
        return move[1]

    # If it is not X's turn to play, it is O's, which is the min player trying to minimize the score
    move = MIN_VALUE(board)
    return move[1]



def MIN_VALUE(board):
    # Stops the recursive nature of the function once the end result has been reveived
    if terminal(board):
        return [utility(board), (0,0)]

    # Initializes a variable used to keep track of the smallest utility
    v = [2, (0,0)]

    for action in actions(board):
        # Initializes the variable which will be used to check if v has changed in order to know which action to return
        c = v[0]

        # Simulates the next players turn and causes a recursive nature in oder to find what the end state of that path's utility is
        
        v[0] = min(v[0], MAX_VALUE(result(board, action))[0])

        # If v is no longer equal to c, that means the action which leads to the lowest utility has changed
        if v[0] != c:
            # Keeps track of the action with the lowest utility
            v[1] = action
    
    return v


def MAX_VALUE(board):
    # Stops the recursive nature of the function once the end result has been reveived
    if terminal(board):
        return [utility(board), (0,0)]

    # Initializes a variable used to keep track of the greatest utility
    v = [-2, (0, 0)]

    for action in actions(board):
        # Initializes the variable which will be used to check if v has changed in order to know which action to return
        c = v[0]

        # Simulates the next players turn and causes a recursive nature in oder to find what the end state of that path's utility is
        v[0] = max(v[0], MIN_VALUE(result(board, action))[0])

        # If v is no longer equal to c, that means the action which leads to the highest utility has changed
        if v[0] != c:
            # Keeps track of the action with the highest utility
            v[1] = action
    
    return v
