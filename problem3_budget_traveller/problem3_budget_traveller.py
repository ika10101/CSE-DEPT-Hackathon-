"""
Problem 3: Budget Traveller with Coupons
Input:
  N M
  K C
  M lines: u v price
Cities are numbered 1..N. At most K intermediate stops means at most K+1 flights.
Run with optional graph visualization:
  python problem3_budget_traveller.py --visualize
"""
import argparse
import csv


def cheapest_flight(n, flights, k, coupons):
    if n < 1 or k < 0 or coupons < 0:
        return -1, []

    max_flights = k + 1
    inf = float("inf")

    # dp[s][v][c]: minimum cost to reach v using exactly s flights
    # and exactly c coupons.
    dp = [[[inf] * (coupons + 1) for _ in range(n + 1)]
          for _ in range(max_flights + 1)]
    parent = [[[None] * (coupons + 1) for _ in range(n + 1)]
              for _ in range(max_flights + 1)]
    dp[0][1][0] = 0

    for s in range(1, max_flights + 1):
        for u, v, price in flights:
            for used in range(coupons + 1):
                previous = dp[s - 1][u][used]
                if previous == inf:
                    continue

                # Pay full fare.
                cost = previous + price
                if cost < dp[s][v][used]:
                    dp[s][v][used] = cost
                    parent[s][v][used] = (u, used, price, False)

                # Use one coupon on this flight.
                if used < coupons:
                    cost = previous + price // 2
                    if cost < dp[s][v][used + 1]:
                        dp[s][v][used + 1] = cost
                        parent[s][v][used + 1] = (
                            u, used, price, True
                        )

    best = (inf, None, None)
    for s in range(max_flights + 1):
        for used in range(coupons + 1):
            cost = dp[s][n][used]
            if cost < best[0]:
                best = (cost, s, used)

    if best[0] == inf:
        return -1, []

    cost, s, used = best
    path = []
    city = n
    while s > 0:
        item = parent[s][city][used]
        if item is None:
            # This should not happen for a reachable state.
            return -1, []
        previous_city, previous_used, price, discounted = item
        path.append((previous_city, city, price, discounted))
        city = previous_city
        used = previous_used
        s -= 1
    path.reverse()
    return int(cost), path


def save_path(path, filename="flight_path.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["From", "To", "Original Price",
                         "Coupon Used", "Final Price"])
        for u, v, price, coupon in path:
            writer.writerow([u, v, price, "Yes" if coupon else "No",
                             price // 2 if coupon else price])


def visualize(n, flights, path):
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print("Visualization needs networkx and matplotlib:")
        print("pip install networkx matplotlib")
        return

    graph = nx.DiGraph()
    graph.add_nodes_from(range(1, n + 1))
    for u, v, price in flights:
        graph.add_edge(u, v, price=price)

    chosen = {(u, v) for u, v, _, _ in path}
    pos = nx.spring_layout(graph, seed=7)
    node_colors = [
        "green" if v == 1 else "red" if v == n
        else "orange" if any(v in edge for edge in chosen)
        else "lightblue"
        for v in graph.nodes()
    ]
    edge_colors = [
        "gold" if (u, v) in chosen and
        any(a == u and b == v and coupon for a, b, _, coupon in path)
        else "blue" if (u, v) in chosen else "gray"
        for u, v in graph.edges()
    ]
    nx.draw_networkx(graph, pos, node_color=node_colors,
                     edge_color=edge_colors, arrows=True)
    labels = {(u, v): str(data["price"])
              for u, v, data in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.title("Flights: selected route in blue, coupon flight in gold")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()

    n, m = map(int, input("Enter N M: ").split())
    k, c = map(int, input("Enter K C: ").split())
    flights = []
    for _ in range(m):
        u, v, price = map(int, input().split())
        if not (1 <= u <= n and 1 <= v <= n) or price < 0:
            raise ValueError("Invalid flight: cities must be 1..N and price >= 0.")
        flights.append((u, v, price))

    cost, path = cheapest_flight(n, flights, k, c)
    print("Minimum cost:", cost)
    if cost != -1:
        for u, v, price, coupon in path:
            final_price = price // 2 if coupon else price
            print(f"{u} -> {v}: {price} -> {final_price}; "
                  f"coupon={'Yes' if coupon else 'No'}")
        save_path(path)
        print("Path saved to flight_path.csv")
    if args.visualize:
        visualize(n, flights, path)
