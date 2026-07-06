import numpy as np
import tkinter as tk
import random
from tkinter import messagebox

# game state
board = np.zeros((3,3))
difficulty = "hard"

player_score = 0
ai_score = 0

# check winner
def check_winner(b):
    for i in range(3):
        if abs(sum(b[i,:])) == 3:
            return np.sign(sum(b[i,:]))
        if abs(sum(b[:,i])) == 3:
            return np.sign(sum(b[:,i]))

    diag1 = b[0,0] + b[1,1] + b[2,2]
    diag2 = b[0,2] + b[1,1] + b[2,0]

    if abs(diag1) == 3:
        return np.sign(diag1)
    if abs(diag2) == 3:
        return np.sign(diag2)

    return 0

# check draw
def is_full(b):
    return not (b == 0).any()

# EASY AI
def ai_move_easy():
    empty = list(zip(*np.where(board == 0)))
    if empty:
        move = random.choice(empty)
        board[move] = 1
        buttons[move[0]][move[1]]["text"] = "O"

# MINIMAX AI
def minimax(b, is_max):
    winner = check_winner(b)
    if winner == 1: return 1
    if winner == -1: return -1
    if is_full(b): return 0

    if is_max:
        best = -100
        for i in range(3):
            for j in range(3):
                if b[i][j] == 0:
                    b[i][j] = 1
                    score = minimax(b, False)
                    b[i][j] = 0
                    best = max(best, score)
        return best
    else:
        best = 100
        for i in range(3):
            for j in range(3):
                if b[i][j] == 0:
                    b[i][j] = -1
                    score = minimax(b, True)
                    b[i][j] = 0
                    best = min(best, score)
        return best

# HARD AI
def ai_move_hard():
    best_score = -100
    move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 1
                score = minimax(board, False)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    move = (i, j)

    if move:
        board[move] = 1
        buttons[move[0]][move[1]]["text"] = "O"

# AI turn handler
def ai_turn():
    if difficulty == "easy":
        ai_move_easy()
    else:
        ai_move_hard()

    check_game_after_ai()

# check after AI move
def check_game_after_ai():
    global ai_score

    if check_winner(board) == 1:
        ai_score += 1
        messagebox.showinfo("Game Over", f"AI Wins!\nScore: You {player_score} - AI {ai_score}")
        reset()
        return

    if is_full(board):
        messagebox.showinfo("Game Over", "Draw!")
        reset()

# player move
def click(i, j):
    global player_score

    if board[i][j] == 0:
        board[i][j] = -1
        buttons[i][j]["text"] = "X"

        if check_winner(board) == -1:
            player_score += 1
            messagebox.showinfo("Game Over", f"You Win!\nScore: You {player_score} - AI {ai_score}")
            reset()
            return

        if is_full(board):
            messagebox.showinfo("Game Over", "Draw!")
            reset()
            return

        # delay AI move
        root.after(500, ai_turn)

# reset game
def reset():
    global board
    board = np.zeros((3,3))
    for row in buttons:
        for btn in row:
            btn["text"] = ""

# difficulty buttons
def set_easy():
    global difficulty
    difficulty = "easy"

def set_hard():
    global difficulty
    difficulty = "hard"

# UI setup
root = tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("300x400")
root.configure(bg="#111")

# game buttons
buttons = []
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(root, text="", width=5, height=2,
                        font=("Arial", 24),
                        bg="#222", fg="white",
                        command=lambda i=i, j=j: click(i,j))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

# control buttons
tk.Button(root, text="Easy", command=set_easy, bg="green", fg="white").grid(row=3, column=0, pady=10)
tk.Button(root, text="Restart", command=reset, bg="blue", fg="white").grid(row=3, column=1)
tk.Button(root, text="Hard", command=set_hard, bg="red", fg="white").grid(row=3, column=2)

root.mainloop()