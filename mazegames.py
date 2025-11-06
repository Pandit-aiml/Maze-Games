import tkinter as tk
from tkinter import messagebox
import random

ROWS, COLS = 10, 10
CELL_SIZE = 50

maze = [[0 if random.random() > 0.3 else 1 for _ in range(COLS)] for _ in range(ROWS)]
maze[0][0] = 0
maze[ROWS-1][COLS-1] = 0

root = tk.Tk()
root.title("Spaceship Maze Game")
canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
canvas.pack()

rects = [[None]*COLS for _ in range(ROWS)]
for r in range(ROWS):
    for c in range(COLS):
        color = "black" if maze[r][c]==1 else "white"
        rects[r][c] = canvas.create_rectangle(c*CELL_SIZE, r*CELL_SIZE,
                                              (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                                              fill=color, outline="gray")

goal = (ROWS-1, COLS-1)
canvas.create_rectangle(goal[1]*CELL_SIZE, goal[0]*CELL_SIZE,
                        (goal[1]+1)*CELL_SIZE, (goal[0]+1)*CELL_SIZE,
                        fill="green")

player_pos = [0,0]
player = canvas.create_oval(5,5,CELL_SIZE-5,CELL_SIZE-5, fill="blue")

def move_player(event):
    dr, dc = 0, 0
    if event.keysym == "Up": dr=-1
    elif event.keysym=="Down": dr=1
    elif event.keysym=="Left": dc=-1
    elif event.keysym=="Right": dc=1
    nr, nc = player_pos[0]+dr, player_pos[1]+dc
    if 0<=nr<ROWS and 0<=nc<COLS and maze[nr][nc]==0:
        player_pos[0], player_pos[1] = nr, nc
        canvas.coords(player, nc*CELL_SIZE+5, nr*CELL_SIZE+5, (nc+1)*CELL_SIZE-5, (nr+1)*CELL_SIZE-5)
        if (nr,nc) == goal:
            messagebox.showinfo("You Win!", "Your spaceship reached the exit!")

root.bind("<Key>", move_player)
root.mainloop()
