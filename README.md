# CSE Dept Hackathon – DSA Problems (V SEM 2026-2027)

| Folder | Problem | Language |
|---|---|---|
| `problem1_maze/` | Maze with Keys and Doors (BFS over position + key bitmask) | Python |
| `problem2_closest_pair/` | Closest Pair of Points (brute force vs divide & conquer) | Python |
| `problem3_budget_traveller/` | Budget Traveller with Coupons (DP over flights / coupons) | Python |
| `problem4_exam_scheduling/` | Exam Timetable Scheduling (DSatur greedy + exact backtracking) | Java (+ Python visualizer) |
| `docs/` | Problem statements and detailed README (PDF) | – |

## Running

```bash
python problem1_maze/problem1_maze.py [--visualize]
python problem2_closest_pair/problem2_closest_pair.py [--visualize | --benchmark]
python problem3_budget_traveller/problem3_budget_traveller.py [--visualize]

cd problem4_exam_scheduling
javac Problem4ExamScheduling.java && java Problem4ExamScheduling
python visualize_problem4.py   # after running the Java program
```

Optional visualization dependencies: `pip install matplotlib networkx`.

See `docs/README.pdf` for full details.
