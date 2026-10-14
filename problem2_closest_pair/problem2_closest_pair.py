"""
Problem 2: Closest Pair of Points
Generates N random points, runs brute force and divide-and-conquer,
checks that both distances agree, and optionally plots the result.

Examples:
  python problem2_closest_pair.py
  python problem2_closest_pair.py --visualize
  python problem2_closest_pair.py --benchmark
"""
import argparse
import math
import random
import time


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def brute_force(points):
    if len(points) < 2:
        return None, None
    best_d = float("inf")
    best_pair = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if d < best_d:
                best_d, best_pair = d, (points[i], points[j])
    return best_d, best_pair


def divide_and_conquer(points):
    if len(points) < 2:
        return None, None

    # Handle duplicate coordinates explicitly; distance is then zero.
    seen = set()
    for p in points:
        if p in seen:
            return 0.0, (p, p)
        seen.add(p)

    px = sorted(points, key=lambda p: (p[0], p[1]))
    py = sorted(points, key=lambda p: (p[1], p[0]))

    def solve(x_sorted, y_sorted):
        n = len(x_sorted)
        if n <= 3:
            return brute_force(x_sorted)

        mid = n // 2
        left_x = x_sorted[:mid]
        right_x = x_sorted[mid:]
        split_x = right_x[0][0]

        # Duplicates were handled above, so coordinate tuples are unique.
        left_points = set(left_x)
        left_y = [p for p in y_sorted if p in left_points]
        right_y = [p for p in y_sorted if p not in left_points]

        d_left, pair_left = solve(left_x, left_y)
        d_right, pair_right = solve(right_x, right_y)

        if d_left <= d_right:
            best_d, best_pair = d_left, pair_left
        else:
            best_d, best_pair = d_right, pair_right

        strip = [p for p in y_sorted if abs(p[0] - split_x) < best_d]
        for i in range(len(strip)):
            # In y-sorted order, only the next 7 points need checking.
            for j in range(i + 1, min(i + 8, len(strip))):
                if strip[j][1] - strip[i][1] >= best_d:
                    break
                d = dist(strip[i], strip[j])
                if d < best_d:
                    best_d, best_pair = d, (strip[i], strip[j])
        return best_d, best_pair

    return solve(px, py)


def run_one(points):
    start = time.perf_counter()
    d1, pair1 = brute_force(points)
    brute_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    d2, pair2 = divide_and_conquer(points)
    divide_ms = (time.perf_counter() - start) * 1000

    print("Brute Force:", "No pair" if pair1 is None else
          f"distance={d1:.6f}, pair={pair1}")
    print("Divide and Conquer:", "No pair" if pair2 is None else
          f"distance={d2:.6f}, pair={pair2}")
    print(f"Execution time: brute force={brute_ms:.3f} ms, "
          f"divide-and-conquer={divide_ms:.3f} ms")
    if d1 is not None and d2 is not None:
        print("Distances agree:", math.isclose(d1, d2, rel_tol=1e-9,
                                               abs_tol=1e-9))
    return d1, pair1, d2, pair2


def visualize(points, pair1, pair2):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Visualization needs matplotlib: pip install matplotlib")
        return

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    plt.figure()
    plt.scatter(xs, ys, label="Points")
    if pair1:
        plt.plot([pair1[0][0], pair1[1][0]],
                 [pair1[0][1], pair1[1][1]],
                 marker="o", label="Brute force pair")
    if pair2:
        plt.plot([pair2[0][0], pair2[1][0]],
                 [pair2[0][1], pair2[1][1]],
                 marker="x", label="Divide-and-conquer pair")
    plt.title("Closest pair of points")
    plt.legend()
    plt.grid(True)
    plt.show()


def benchmark():
    sizes = [50, 100, 200, 400, 800, 1200]
    brute_times, divide_times = [], []
    for n in sizes:
        points = [(random.random() * 10000, random.random() * 10000)
                  for _ in range(n)]
        t = time.perf_counter()
        brute_force(points)
        brute_times.append((time.perf_counter() - t) * 1000)
        t = time.perf_counter()
        divide_and_conquer(points)
        divide_times.append((time.perf_counter() - t) * 1000)
        print(f"N={n}: brute={brute_times[-1]:.3f} ms, "
              f"divide={divide_times[-1]:.3f} ms")

    try:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(sizes, brute_times, marker="o", label="Brute force")
        plt.plot(sizes, divide_times, marker="o",
                 label="Divide and conquer")
        plt.xlabel("Number of points (N)")
        plt.ylabel("Execution time (ms)")
        plt.title("Closest-pair performance")
        plt.legend()
        plt.grid(True)
        plt.show()
    except ImportError:
        print("Install matplotlib to plot benchmark results.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--visualize", action="store_true")
    parser.add_argument("--benchmark", action="store_true")
    args = parser.parse_args()

    if args.benchmark:
        benchmark()
    else:
        n = int(input("Enter number of points N: "))
        if n < 2:
            print("At least 2 points are required.")
        else:
            points = [(random.randint(0, 1000), random.randint(0, 1000))
                      for _ in range(n)]
            _, pair1, _, pair2 = run_one(points)
            if args.visualize:
                visualize(points, pair1, pair2)
