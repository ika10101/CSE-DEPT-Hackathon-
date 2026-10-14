"""
Problem 1: Maze with Keys and Doors
Input:
  N
  N rows, each row either space-separated cells or a compact string.
Example:
  4
  S . a #
  # # . #
  . . A E
  . . . .
Run with optional visualization:
  python problem1_maze.py --visualize
"""
from collections import deque
import argparse
import csv


def read_grid():
    n = int(input("Enter grid size N: ").strip())
    grid = []
    for _ in range(n):
        line = input().strip()
        cells = line.split() if " " in line else list(line)
        if len(cells) != n:
            raise ValueError(f"Each row must contain exactly {n} cells.")
        grid.append(cells)
    return grid


def solve_maze(grid):
    n = len(grid)
    if n == 0 or any(len(row) != n for row in grid):
        raise ValueError("The maze must be a non-empty square grid.")

    starts, ends = [], []
    for r in range(n):
        for c in range(n):
            if grid[r][c] == "S":
                starts.append((r, c))
            elif grid[r][c] == "E":
                ends.append((r, c))

    if len(starts) != 1 or len(ends) != 1:
        return -1, []

    start, end = starts[0], ends[0]
    # Each state includes the keys currently held.
    start_state = (start[0], start[1], 0)
    queue = deque([start_state])
    parent = {start_state: None}
    distance = {start_state: 0}
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    target_state = None

    while queue:
        r, c, keys = queue.popleft()
        state = (r, c, keys)

        if (r, c) == end:
            target_state = state
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n and 0 <= nc < n):
                continue

            cell = grid[nr][nc]
            if cell == "#":
                continue

            if cell in "ABCDF":
                required = 1 << (ord(cell.lower()) - ord("a"))
                if not (keys & required):
                    continue

            new_keys = keys
            if "a" <= cell <= "f":
                new_keys |= 1 << (ord(cell) - ord("a"))

            next_state = (nr, nc, new_keys)
            if next_state not in parent:
                parent[next_state] = state
                distance[next_state] = distance[state] + 1
                queue.append(next_state)

    if target_state is None:
        return -1, []

    path = []
    state = target_state
    while state is not None:
        path.append((state[0], state[1]))
        state = parent[state]
    path.reverse()
    return distance[target_state], path


def save_path_csv(grid, path, filename="maze_path.csv"):
    marked = [row[:] for row in grid]
    for r, c in path:
        if marked[r][c] == ".":
            marked[r][c] = "x"
        # Keep S, E, keys and doors visible and identifiable.
    with open(filename, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(marked)


def visualize(grid, path):
    try:
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
        from matplotlib.patches import Patch
    except ImportError:
        print("Visualization needs matplotlib: pip install matplotlib")
        return

    n = len(grid)
    path_set = set(path)
    fig, ax = plt.subplots()
    ax.set_xlim(0, n)
    ax.set_ylim(n, 0)
    ax.set_aspect("equal")
    ax.set_xticks(range(n + 1))
    ax.set_yticks(range(n + 1))
    ax.grid(True)

    for r in range(n):
        for c in range(n):
            cell = grid[r][c]
            color = "white"
            if cell == "#":
                color = "black"
            elif cell == "S":
                color = "green"
            elif cell == "E":
                color = "red"
            elif cell.isalpha() and cell.islower():
                color = "#80cbc4"
            elif cell.isalpha() and cell.isupper():
                color = "#ffcc80"
            elif (r, c) in path_set:
                color = "#90caf9"
            ax.add_patch(plt.Rectangle((c, r), 1, 1, facecolor=color,
                                       edgecolor="gray"))
            ax.text(c + 0.5, r + 0.5, cell, ha="center", va="center",
                    color="white" if cell == "#" else "black")
    if path:
        xs = [c + 0.5 for r, c in path]
        ys = [r + 0.5 for r, c in path]
        ax.plot(xs, ys, color="blue", linewidth=2, marker="o")
    ax.set_title("Maze shortest path")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()

    maze = read_grid()
    steps, path = solve_maze(maze)
    print("Shortest path:", steps)
    if steps >= 0:
        save_path_csv(maze, path)
        print("Path saved to maze_path.csv")
    if args.visualize:
        visualize(maze, path)
