import math

# Board initialization
def create_board():
    return [" " for _ in range(9)]

def print_board(board):
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print("| " + " | ".join(row) + " |")

def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]

def winner(board):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] != " ":
            return board[cond[0]]
    return None

def is_full(board):
    return " " not in board

# Minimax with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    win = winner(board)
    if win == "X":
        return 1
    elif win == "O":
        return -1
    elif is_full(board):
        return 0

    if maximizing_player:
        max_eval = -math.inf
        for move in available_moves(board):
            board[move] = "X"
            eval = minimax(board, depth+1, alpha, beta, False)
            board[move] = " "
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in available_moves(board):
            board[move] = "O"
            eval = minimax(board, depth+1, alpha, beta, True)
            board[move] = " "
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = None
    for m in available_moves(board):
        board[m] = "X"
        move_val = minimax(board, 0, -math.inf, math.inf, False)
        board[m] = " "
        if move_val > best_val:
            best_val = move_val
            move = m
    return move

# Game loop
def play_game():
    board = create_board()
    print_board(board)

    while True:
        # Human move
        human_move = int(input("Enter your move (0-8): "))
        if board[human_move] == " ":
            board[human_move] = "O"
        else:
            print("Invalid move. Try again.")
            continue

        print_board(board)
        if winner(board) or is_full(board):
            break

        # AI move
        ai_move = best_move(board)
        board[ai_move] = "X"
        print("AI chooses:", ai_move)
        print_board(board)

        if winner(board) or is_full(board):
            break

    if winner(board):
        print("Winner:", winner(board))
    else:
        print("It's a draw!")

# Run the game
if __name__ == "__main__":
    play_game()
