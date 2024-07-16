import termcolor
from copy import deepcopy
import random

EMPTY_TILE = 0
X_PIECE = 1
O_PIECE = 2
NO_WINNER = "NO_WINNER"

def make_check_winner(seq):
    def check_winner(board):
        height = len(board)
        if height == 0:
            return NO_WINNER
        width = len(board[0])

        for row in range(height):
            for col in range(width):
                start = get_piece(board, row, col)
                for dr, dc in seq:
                    if not (0 <= row + dr < height):
                        break
                    if not (0 <= col + dc < width):
                        break
                    if start != get_piece(board, row + dr, col + dc):
                        break
                else:
                    if start != EMPTY_TILE:
                        return start
        return NO_WINNER
    return check_winner

def get_piece(board, row, column):
    """
    Retrieves the piece at the given row and column in the board.

    Args:
        board (list of list of int): 
            A 2D list representing the board and the pieces on it.
        row (int): 
            The row index of the piece to retrieve.
        column (int): 
            The column index of the piece to retrieve.
    """
    # YOUR CODE HERE
    return board[-row-1][column]

def print_space():
    """Prints a space, without printing a new line."""
    print(' ', end='')

def our_print_board(board):
    """Prints a visual representation of the board."""
    for row in board:
        for tile in row:
            print_tile(tile)
            print_space()
        print()

def print_tile(tile):
    """
    Given a numerical tile, prints its visual representation.

    Args:
        tile (EMPTY_TILE, X_PIECE, or O_PIECE): 
            The tile to print.
    """
    if tile == EMPTY_TILE:
        # No coloring here because we don't know if it's dark or light mode.
        print("·", end = '')
    elif tile == X_PIECE:
        print(termcolor.colored('X', 'red'), end = '')
    elif tile == O_PIECE:
        print(termcolor.colored('O', 'blue'), end = '')
    else:
        raise RuntimeError(f"Error: the tile given was not 0, 1, or 2 (got {tile})")


class ConnectFour:
    def __init__(self, h, w, ai_first = True):
        self.h = h
        self.w = w
        self.state = [['.' for _ in range(self.w)] for _ in range(self.h)]  # Initialize your game state here
        self.ai_first = ai_first
        self.current_player = '1'  # Starting player
    
    def possible_moves(self):
        # Return a list of possible moves from the current state
        moves = []
        highest = self.highest_dot_indices(self.state)
        for i in range(len(highest)):
            if highest[i] is not None:
                moves.append((highest[i], i))
        return moves
    
    def highest_dot_indices(self, matrix):
        n = len(matrix)
        m = len(matrix[0]) if matrix else 0
        
        if n == 0 or m == 0:
            return []

        highest_indices = [None] * m  # Initialize with None (indicating no '.' found in the column)

        for col in range(m):
            highest_index = None  # Start with None for this column
            for row in range(n):
                if matrix[row][col] == '.':
                    highest_index = row  # Update with the current row index
            highest_indices[col] = highest_index  # Update the highest index found in this column

        return highest_indices
    
    def make_move(self, move):
        # Apply the given move to the current state
        x, y = move
        self.state[x][y] = self.current_player
        self.current_player = '2' if self.current_player == '1' else '1'  # Switch player turn (1 <-> 2)
    
    def is_over(self):
        # Check if the game is over
        return self.check_win('1') or self.check_win('2') or not self.possible_moves()
        
    def show(self):
        # Display the current state of the game
        for row in self.state:
            print(' '.join(row))
    
    def scoring(self):

        # pruning tip - check when states are duds and cannot be won 

        # Compute and return the current score from the perspective of the current player
        # if self.check_win('1'):
        #     return 1 if self.current_player == '1' else -1
        # elif self.check_win('2'):
        #     return 1 if self.current_player == '2' else -1
        # else:
        #     return 0
        if self.check_win('1'):
            if self.ai_first:
                return 1
            else:
                return -1
        if self.check_win('2'):
            if self.ai_first:
                return -1
            else:
                return 1
        return 0
    
    
    def check_win(self, player):
        # Check for a win condition for the given player
        for row in range(self.h):
            for col in range(self.w - 3):
                if all(self.state[row][col + i] == player for i in range(4)):
                    return True
        
        for col in range(self.w):
            for row in range(self.h - 3):
                if all(self.state[row + i][col] == player for i in range(4)):
                    return True
        
        for row in range(3, self.h):
            for col in range(self.w - 3):
                if all(self.state[row - i][col + i] == player for i in range(4)):
                    return True
        
        for row in range(self.h - 3):
            for col in range(self.w - 3):
                if all(self.state[row + i][col + i] == player for i in range(4)):
                    return True
        
        return False
    
    def minimax(self, depth):
        # print(self.current_player)
        

        def max_value(state, alpha, beta, depth):
            if depth <= 0 or state.is_over():
                return state.scoring()
            v = float('-inf')
            for move in state.possible_moves():
                new_state = deepcopy(state)
                new_state.make_move(move)
                v = max(v, min_value(new_state, alpha, beta, depth - 1))
                alpha = max(alpha, v)  # Update alpha with the current best score
                if alpha >= beta:
                    break  # Prune if the score exceeds beta
            return v
        
        def min_value(state, alpha, beta, depth):
            # print(state.check_win('1'), state.current_player, state.scoring())
            if depth <= 0 or state.is_over():
                return state.scoring()
            v = float('inf')
            for move in state.possible_moves():
                new_state = deepcopy(state)
                new_state.make_move(move)
                # print('bruhh')
                # print('new score', new_state.scoring())
                v = min(v, max_value(new_state, alpha, beta, depth - 1))
                beta = min(beta, v)  # Update beta with the current worst score
                if beta <= alpha:
                    break  # Prune if the score is less than alpha
            return v

        best_score = float('-inf')  # Use current state score as initial value
        best_move = self.possible_moves()[0]
        

        scores = []

        for move in self.possible_moves():
            new_state = deepcopy(self)
            new_state.make_move(move)
            score = min_value(new_state, best_score, float('inf'), depth - 1)  # Adjust alpha to current best score
            if score >= best_score:
                best_score = score
            scores.append(score)
        best_indices = []
        for i in range(len(scores)):
            if scores[i] == best_score:
                best_indices.append(i)

        rand_idx = random.choice(best_indices)
    
        # print(scores)
        return self.possible_moves()[rand_idx]


def playGame():
    player = 1
    ai_first = player == 1
    depth = 7
    game = ConnectFour(h=6, w=7, ai_first=ai_first)
    game.show()
    while not game.is_over():
        next_row, next_column = 'h', 'h'
        if player == 0:
            possible_moves = game.possible_moves()
            valid_moves = [x[1] for x in possible_moves]
            print(f'Valid Moves: {valid_moves}')
            move = (0, 0)
            while True:
                try:
                    next_column = int(input('What column'))
                    if next_column in valid_moves:
                        break
                    else:
                        raise ValueError()
                except:
                    print('Choose a valid move')
            # next_column = int(input('What column'))
            for i in range(len(valid_moves)):
                if possible_moves[i][1] == next_column:
                    next_row = possible_moves[i][0]

                
            print(f'Column {next_column}')
            move = (next_row, next_column)
            game.make_move(move)
            player = 1
            print('Human Move Made', move)
        else:
            print('AI Thinking...')
            best_move = game.minimax(depth)
            game.make_move(best_move)
            player = 0
            print('AI Move Made', best_move)
        game.show()
    if game.check_win('1'):
        print('AI Wins!')
    elif game.check_win('2'):
        print('Player Wins!')
    else:
        print('Tie!')
