import numpy as np
import tkinter as tk
from tkinter import messagebox

# create board
board = np.zeros((3,3))

# check winner
def check_winner(b):
    for i in range(3):
        if abs(sum(b[i,:])) == 3 or abs(sum(b[:,i])) == 3:
            return np.sign(sum(b[i,:]) or sum(b[:,i]))
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

# AI move
def ai_move():
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

# player move
def click(i, j):
    if board[i][j] == 0:
        board[i][j] = -1
        buttons[i][j]["text"] = "X"

        if check_winner(board) == -1:
            messagebox.showinfo("Game Over", "You Win!")
            reset()
            return

        if is_full(board):
            messagebox.showinfo("Game Over", "Draw!")
            reset()
            return

        ai_move()

        if check_winner(board) == 1:
            messagebox.showinfo("Game Over", "AI Wins!")
            reset()
            return

        if is_full(board):
            messagebox.showinfo("Game Over", "Draw!")
            reset()

# reset game
def reset():
    global board
    board = np.zeros((3,3))
    for row in buttons:
        for btn in row:
            btn["text"] = ""

# UI
root = tk.Tk()
root.title("Tic Tac Toe AI")

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(root, text="", width=10, height=3,
                        font=("Arial", 20),
                        command=lambda i=i, j=j: click(i,j))
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

root.mainloop()