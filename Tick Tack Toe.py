import tkinter as tk

# Define constants
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
AI_PLAYER = PLAYER_X  # AI plays as PLAYER_X
HUMAN_PLAYER = PLAYER_O

# Define the game board
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

# Function to check if the game is over
def game_over(board):
    # Check rows
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != EMPTY:
            return True, row[0]

    # Check columns
    for col in range(len(board)):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] != EMPTY):
            return True, board[0][col]

    # Check diagonals
    if (board[0][0] == board[1][1] == board[2][2] or
            board[0][2] == board[1][1] == board[2][0]) and (board[1][1] != EMPTY):
        return True, board[1][1]

    # Check for draw
    if all(all(cell != EMPTY for cell in row) for row in board):
        return True, None

    return False, None

# Function to print the board on the GUI
def update_board(board, buttons):
    for i in range(3):
        for j in range(3):
            cell_button = buttons[i][j]
            if board[i][j] == PLAYER_X:
                cell_button.config(text="X", state=tk.DISABLED)
            elif board[i][j] == PLAYER_O:
                cell_button.config(text="O", state=tk.DISABLED)
            else:
                cell_button.config(text="", state=tk.NORMAL)

# Function for AI's move using minimax with alpha-beta pruning
def ai_move(board, depth, alpha, beta, is_maximizing):
    game_over_flag, winner = game_over(board)
    if game_over_flag:
        if winner == AI_PLAYER:
            return 10 - depth
        elif winner == HUMAN_PLAYER:
            return depth - 10
        else:
            return 0

    possible_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.append((i, j))

    if is_maximizing:
        best_score = -float('inf')
        for move in possible_moves:
            board[move[0]][move[1]] = AI_PLAYER
            score = ai_move(board, depth + 1, alpha, beta, False)
            board[move[0]][move[1]] = EMPTY
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for move in possible_moves:
            board[move[0]][move[1]] = HUMAN_PLAYER
            score = ai_move(board, depth + 1, alpha, beta, True)
            board[move[0]][move[1]] = EMPTY
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

# Function to find the best move for AI
def find_best_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI_PLAYER
                score = ai_move(board, 0, -float('inf'), float('inf'), False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# Main game loop
def main():
    def check_game_over(buttons, game_label):
     game_over_flag, winner = game_over(board)
     if game_over_flag:
         for row in buttons:
            for button in row:
               button.config(state=tk.DISABLED)
         if winner is None:
          message = "It's a draw!"
          message_label = tk.Label(window, text=message, font=("Helvetica", 22, "bold"), fg="red")
          message_label.grid(row=1, column=1, rowspan=1, columnspan=1)  # Place label in the center
         elif winner == AI_PLAYER:
          message = "Opponent wins!"
          message_label = tk.Label(window, text=message, font=("Helvetica", 16, "bold"), fg="red")
          message_label.grid(row=1, column=1, rowspan=1, columnspan=1)  # Place label in the center
         else:
          message = "You win!"
          message_label = tk.Label(window, text=message, font=("Helvetica", 16, "bold"), fg="red")
          message_label.grid(row=1, column=1, rowspan=1, columnspan=1)  # Place label in the center  
     

    def make_ai_move():
        move = find_best_move(board)
        board[move[0]][move[1]] = AI_PLAYER
        update_board(board, buttons)
        check_game_over(buttons, game_label)

    window = tk.Tk()
    window.title("Tic-Tac-Toe")

    # Create buttons for the game board
    buttons = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            button = tk.Button(window, text="", width=10, height=5, font=("Helvetica", 20),
                               command=lambda i=i, j=j: human_move(button, i, j, buttons, game_label))
            button.grid(row=i, column=j)
            buttons[i][j] = button

    # Label to display game status
    global game_label
    game_label = tk.Label(window, text="", font=("Helvetica", 16))
    game_label.grid(row=3, columnspan=3)

    # Initialize current player
    global current_player
    current_player = AI_PLAYER

    def human_move(cell_button, i, j, buttons, game_label):
        if board[i][j] == EMPTY:
            board[i][j] = HUMAN_PLAYER
            update_board(board, buttons)
            check_game_over(buttons, game_label)
            make_ai_move()

    window.mainloop()

if __name__ == "__main__":
    main()

