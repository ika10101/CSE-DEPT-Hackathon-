"""
Optional visualization helper for Problem 4's Java output.
Run the Java program first, then:
  pip install pandas matplotlib networkx
  python visualize_problem4.py
"""
import csv
import matplotlib.pyplot as plt
import networkx as nx


def main():
    graph = nx.Graph()
    with open("conflicts.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            graph.add_edge(int(row["Course1"]), int(row["Course2"]))

    slot_by_course = {}
    with open("timetable.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            slot_by_course[int(row["Course"])] = int(row["Slot"])

    graph.add_nodes_from(slot_by_course)
    pos = nx.spring_layout(graph, seed=7)
    colors = [slot_by_course.get(v, 1) for v in graph.nodes()]
    nx.draw_networkx(graph, pos, node_color=colors, cmap=plt.cm.Set3,
                     with_labels=True, edge_color="gray")
    plt.title("Exam conflict graph (node colour = assigned slot)")
    plt.axis("off")
    plt.show()

    slots = sorted(set(slot_by_course.values()))
    plt.figure()
    for slot in slots:
        courses = [v for v, s in slot_by_course.items() if s == slot]
        plt.scatter([slot] * len(courses), courses, label=f"Slot {slot}")
        for course in courses:
            plt.text(slot, course, str(course))
    plt.xlabel("Time slot")
    plt.ylabel("Course")
    plt.title("Exam timetable")
    plt.xticks(slots)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
