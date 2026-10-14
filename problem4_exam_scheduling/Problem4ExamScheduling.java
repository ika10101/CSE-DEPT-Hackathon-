import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

/*
 * Problem 4: Exam Timetable Scheduling
 * Input:
 *   N M R
 *   M lines: u v (1-based course IDs that conflict)
 *
 * Outputs greedy DSatur and exact backtracking timetables.
 * Writes exact timetable to timetable.csv and conflicts to conflicts.csv.
 */
public class Problem4ExamScheduling {
    static int n, m, R;
    static boolean[][] conflict;
    static int[] greedyColor;
    static int[] bestColor;
    static int bestSlots;

    static int degree(int v) {
        int d = 0;
        for (int u = 0; u < n; u++) {
            if (conflict[v][u]) d++;
        }
        return d;
    }

    static int saturation(int v, int[] colors) {
        Set<Integer> seen = new HashSet<>();
        for (int u = 0; u < n; u++) {
            if (conflict[v][u] && colors[u] != -1) {
                seen.add(colors[u]);
            }
        }
        return seen.size();
    }

    static boolean canUse(int v, int slot, int[] colors) {
        int count = 0;
        for (int u = 0; u < n; u++) {
            if (colors[u] == slot) {
                count++;
                if (conflict[v][u]) return false;
            }
        }
        return count < R;
    }

    static int greedyDsatur() {
        int[] colors = new int[n];
        Arrays.fill(colors, -1);
        int usedSlots = 0;

        for (int assigned = 0; assigned < n; assigned++) {
            int chosen = -1;
            int bestSat = -1;
            int bestDeg = -1;

            for (int v = 0; v < n; v++) {
                if (colors[v] != -1) continue;
                int sat = saturation(v, colors);
                int deg = degree(v);
                if (sat > bestSat || (sat == bestSat && deg > bestDeg)) {
                    chosen = v;
                    bestSat = sat;
                    bestDeg = deg;
                }
            }

            boolean placed = false;
            for (int slot = 0; slot < usedSlots; slot++) {
                if (canUse(chosen, slot, colors)) {
                    colors[chosen] = slot;
                    placed = true;
                    break;
                }
            }

            if (!placed && usedSlots < n && R > 0) {
                colors[chosen] = usedSlots;
                usedSlots++;
                placed = true;
            }

            if (!placed) return -1;
        }

        greedyColor = colors;
        return usedSlots;
    }

    static void exactSearch(int assignedCount, int usedSlots, int[] colors) {
        if (assignedCount == n) {
            if (usedSlots < bestSlots) {
                bestSlots = usedSlots;
                bestColor = colors.clone();
            }
            return;
        }

        // Cannot improve the current best if we already use that many slots.
        if (usedSlots >= bestSlots) return;

        // Select the next unassigned course using DSatur.
        int chosen = -1;
        int bestSat = -1;
        int bestDeg = -1;
        for (int v = 0; v < n; v++) {
            if (colors[v] != -1) continue;
            int sat = saturation(v, colors);
            int deg = degree(v);
            if (sat > bestSat || (sat == bestSat && deg > bestDeg)) {
                chosen = v;
                bestSat = sat;
                bestDeg = deg;
            }
        }

        // Try existing slots first. Only introduce the next unused slot,
        // which avoids exploring equivalent permutations of slot labels.
        for (int slot = 0; slot <= usedSlots; slot++) {
            boolean isNew = slot == usedSlots;
            if (isNew && usedSlots + 1 >= bestSlots) continue;
            if (isNew && usedSlots >= n) continue;

            if (canUse(chosen, slot, colors)) {
                colors[chosen] = slot;
                exactSearch(assignedCount + 1,
                            isNew ? usedSlots + 1 : usedSlots, colors);
                colors[chosen] = -1;
            }
        }
    }

    static void printTimetable(int[] colors, int slots) {
        for (int s = 0; s < slots; s++) {
            System.out.print("Slot " + (s + 1) + ": ");
            boolean first = true;
            for (int v = 0; v < n; v++) {
                if (colors[v] == s) {
                    if (!first) System.out.print(", ");
                    System.out.print(v + 1);
                    first = false;
                }
            }
            System.out.println();
        }
    }

    static void saveCsv(int[] colors, int slots) throws IOException {
        try (FileWriter out = new FileWriter("timetable.csv")) {
            out.write("Slot,Hall,Course\n");
            for (int s = 0; s < slots; s++) {
                int hall = 1;
                for (int v = 0; v < n; v++) {
                    if (colors[v] == s) {
                        out.write((s + 1) + "," + hall + "," + (v + 1) + "\n");
                        hall++;
                    }
                }
            }
        }
        try (FileWriter out = new FileWriter("conflicts.csv")) {
            out.write("Course1,Course2\n");
            for (int u = 0; u < n; u++) {
                for (int v = u + 1; v < n; v++) {
                    if (conflict[u][v]) {
                        out.write((u + 1) + "," + (v + 1) + "\n");
                    }
                }
            }
        }
    }

    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        m = sc.nextInt();
        R = sc.nextInt();

        if (n < 0 || m < 0 || R <= 0) {
            System.out.println("Invalid input: N and M must be non-negative, R must be positive.");
            sc.close();
            return;
        }

        conflict = new boolean[n][n];
        for (int i = 0; i < m; i++) {
            int u = sc.nextInt() - 1;
            int v = sc.nextInt() - 1;
            if (u < 0 || u >= n || v < 0 || v >= n || u == v) {
                System.out.println("Invalid conflict edge.");
                sc.close();
                return;
            }
            conflict[u][v] = true;
            conflict[v][u] = true;
        }
        sc.close();

        long start = System.nanoTime();
        int greedySlots = greedyDsatur();
        long greedyMs = (System.nanoTime() - start) / 1_000_000;

        System.out.println("Greedy DSatur slots: " + greedySlots);
        System.out.println("Greedy time: " + greedyMs + " ms");
        if (greedySlots >= 0) printTimetable(greedyColor, greedySlots);

        if (n == 0) {
            System.out.println("Exact slots: 0");
            System.out.println("Optimal: Yes");
            saveCsv(new int[0], 0);
            return;
        }

        // Greedy always gives a valid upper bound when R >= 1.
        bestSlots = greedySlots;
        bestColor = greedyColor.clone();

        start = System.nanoTime();
        int[] current = new int[n];
        Arrays.fill(current, -1);
        exactSearch(0, 0, current);
        long exactMs = (System.nanoTime() - start) / 1_000_000;

        System.out.println("Exact minimum slots: " + bestSlots);
        System.out.println("Exact time: " + exactMs + " ms");
        System.out.println("Optimal: Yes (exact search completed)");
        System.out.println("Exact timetable:");
        printTimetable(bestColor, bestSlots);
        saveCsv(bestColor, bestSlots);
        System.out.println("Saved timetable.csv and conflicts.csv");
    }
}
