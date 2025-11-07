import tkinter as tk
from tkinter import messagebox
import random
import heapq 


ROWS, COLS = 10, 10
CELL_SIZE = 50


maze = [[0 if random.random() > 0.3 else 1 for _ in range(COLS)] for _ in range(ROWS)]
maze[0][0] = 0
maze[ROWS - 1][COLS - 1] = 0

root = tk.Tk()
root.title("Spaceship Maze Game - Dijkstra Edition")

canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
canvas.pack()

rects = [[None] * COLS for _ in range(ROWS)]
for r in range(ROWS):
    for c in range(COLS):
        color = "black" if maze[r][c] == 1 else "white"
        rects[r][c] = canvas.create_rectangle(
            c * CELL_SIZE, r * CELL_SIZE,
            (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
            fill=color, outline="gray"
        )

start = (0, 0)
goal = (ROWS - 1, COLS - 1)


canvas.create_rectangle(goal[1]*CELL_SIZE, goal[0]*CELL_SIZE,
                        (goal[1]+1)*CELL_SIZE, (goal[0]+1)*CELL_SIZE,
                        fill="green")


player_pos = list(start)
player = canvas.create_oval(5, 5, CELL_SIZE - 5, CELL_SIZE - 5, fill="blue")


directions = [(-1,0),(1,0),(0,-1),(0,1)]  

def dijkstra_path(start, goal):
    rows, cols = len(maze), len(maze[0])
    distances = [[float('inf')] * cols for _ in range(rows)]
    prev = [[None] * cols for _ in range(rows)]
    distances[start[0]][start[1]] = 0

    pq = [(0, start)]
    while pq:
        dist, (r, c) = heapq.heappop(pq)
        if (r, c) == goal:
            break
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                new_dist = dist + 1 
                if new_dist < distances[nr][nc]:
                    distances[nr][nc] = new_dist
                    prev[nr][nc] = (r, c)
                    heapq.heappush(pq, (new_dist, (nr, nc)))


    path = []
    node = goal
    while node:
        path.append(node)
        node = prev[node[0]][node[1]]
    path.reverse()
    return path if path[0] == start else None


def auto_move():
    path = dijkstra_path(start, goal)
    if not path:
        messagebox.showwarning("No Path", "No path found in this maze!")
        return

    def step(i=0):
        if i < len(path):
            r, c = path[i]
            canvas.coords(player,
                          c*CELL_SIZE + 5, r*CELL_SIZE + 5,
                          (c+1)*CELL_SIZE - 5, (r+1)*CELL_SIZE - 5)
            root.after(200, step, i+1)
        else:
            messagebox.showinfo("You Win!", "Spaceship reached the destination!")

    step()


button = tk.Button(root, text="Run Dijkstra Path", command=auto_move, bg="lightblue")
button.pack(pady=10)

root.mainloop()
