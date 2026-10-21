import itertools
import math
import random
import time
from functools import lru_cache

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st

st.set_page_config(page_title="TSP Algorithm Lab", page_icon="🧭", layout="wide")
st.title("🧭 Travelling Salesperson Problem — DAA Mini Project")
st.caption("Compare exact algorithms with heuristic and approximation methods.")

st.markdown("""
**Problem:** Find a minimum-cost tour that visits every city exactly once and returns to the start.
This demo uses a complete, symmetric Euclidean distance graph. The MST 2-approximation guarantee
applies when distances satisfy the triangle inequality (as Euclidean distances do).
""")

ALGORITHMS = ["Nearest Neighbour", "MST 2-Approximation", "Held–Karp DP", "Branch and Bound", "Brute Force"]

def make_cities(n, seed):
    rng = random.Random(seed)
    return [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(n)]

def distances_from_points(points):
    n = len(points)
    return [[math.dist(points[i], points[j]) for j in range(n)] for i in range(n)]

def tour_cost(tour, d):
    if len(tour) < 2:
        return 0.0
    return sum(d[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))

def nearest_neighbour(d, start=0):
    n = len(d)
    unvisited = set(range(n))
    unvisited.remove(start)
    tour = [start]
    while unvisited:
        nxt = min(unvisited, key=lambda j: d[tour[-1]][j])
        tour.append(nxt)
        unvisited.remove(nxt)
    return tour, tour_cost(tour, d)

def mst_approximation(d, start=0):
    # Build an MST, then preorder-visit it. For metric TSP this is a 2-approximation.
    n = len(d)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            graph.add_edge(i, j, weight=d[i][j])
    tree = nx.minimum_spanning_tree(graph, weight="weight")
    order = []
    seen = set()
    def preorder(u):
        seen.add(u)
        order.append(u)
        neighbours = sorted(tree.neighbors(u), key=lambda v: d[u][v])
        for v in neighbours:
            if v not in seen:
                preorder(v)
    preorder(start)
    return order, tour_cost(order, d)

def held_karp(d, start=0):
    n = len(d)
    if n <= 1:
        return [start], 0.0
    others = [i for i in range(n) if i != start]
    # dp[(mask, last)] = (cost from start through mask ending at last, predecessor)
    dp = {}
    for j in others:
        dp[(1 << j, j)] = (d[start][j], start)
    for size in range(2, n):
        for subset in itertools.combinations(others, size):
            mask = sum(1 << j for j in subset)
            for last in subset:
                prev_mask = mask ^ (1 << last)
                best_cost, best_prev = min(
                    (dp[(prev_mask, prev)][0] + d[prev][last], prev)
                    for prev in subset if prev != last
                )
                dp[(mask, last)] = (best_cost, best_prev)
    full_mask = sum(1 << j for j in others)
    best_total, last = min((dp[(full_mask, j)][0] + d[j][start], j) for j in others)
    rev = [last]
    mask = full_mask
    while True:
        cost, prev = dp[(mask, last)]
        if prev == start:
            break
        rev.append(prev)
        mask ^= 1 << last
        last = prev
    rev.reverse()
    return [start] + rev, best_total

def branch_and_bound(d, start=0, time_limit=8.0):
    # Exact search with a valid MST-based lower bound; may stop at time limit.
    n = len(d)
    if n <= 2:
        tour = list(range(n))
        return tour, tour_cost(tour, d), True, 0
    all_nodes = set(range(n))
    best_tour, best_cost = nearest_neighbour(d, start)
    path = [start]
    remaining = all_nodes - {start}
    began = time.perf_counter()
    nodes = 0
    timed_out = False

    def mst_cost(nodes_set):
        if len(nodes_set) <= 1:
            return 0.0
        root = next(iter(nodes_set))
        used = {root}
        total = 0.0
        while len(used) < len(nodes_set):
            w, v = min((d[u][v], v) for u in used for v in nodes_set - used)
            total += w
            used.add(v)
        return total

    def lower_bound(current, rem, cost):
        if not rem:
            return cost + d[current][start]
        connector_current = min(d[current][v] for v in rem)
        connector_start = min(d[start][v] for v in rem)
        return cost + mst_cost(rem) + connector_current + connector_start

    def dfs(current, rem, cost):
        nonlocal best_tour, best_cost, nodes, timed_out
        nodes += 1
        if time.perf_counter() - began > time_limit:
            timed_out = True
            return
        if not rem:
            total = cost + d[current][start]
            if total < best_cost:
                best_cost = total
                best_tour = path.copy()
            return
        if lower_bound(current, rem, cost) >= best_cost - 1e-12:
            return
        for nxt in sorted(rem, key=lambda v: d[current][v]):
            path.append(nxt)
            dfs(nxt, rem - {nxt}, cost + d[current][nxt])
            path.pop()
            if timed_out:
                return

    dfs(start, remaining, 0.0)
    return best_tour, best_cost, not timed_out, nodes

def brute_force(d, start=0, time_limit=8.0):
    n = len(d)
    if n <= 2:
        tour = list(range(n))
        return tour, tour_cost(tour, d), True, 0
    others = [i for i in range(n) if i != start]
    best_tour, best_cost = None, float("inf")
    began = time.perf_counter()
    checked = 0
    for perm in itertools.permutations(others):
        if time.perf_counter() - began > time_limit:
            break
        checked += 1
        tour = [start] + list(perm)
        c = tour_cost(tour, d)
        if c < best_cost:
            best_cost, best_tour = c, tour
    complete = best_tour is not None and checked == math.factorial(n - 1)
    if best_tour is None:
        best_tour, best_cost = nearest_neighbour(d, start)
    return best_tour, best_cost, complete, checked

def run_algorithm(name, d, start):
    t0 = time.perf_counter()
    if name == "Nearest Neighbour":
        tour, cost = nearest_neighbour(d, start)
        complete, explored = True, None
    elif name == "MST 2-Approximation":
        tour, cost = mst_approximation(d, start)
        complete, explored = True, None
    elif name == "Held–Karp DP":
        tour, cost = held_karp(d, start)
        complete, explored = True, None
    elif name == "Branch and Bound":
        tour, cost, complete, explored = branch_and_bound(d, start)
    else:
        tour, cost, complete, explored = brute_force(d, start)
    elapsed = time.perf_counter() - t0
    return {"Algorithm": name, "Tour": tour, "Distance": cost, "Time (ms)": elapsed * 1000,
            "Completed": complete, "States / tours checked": explored}

with st.sidebar:
    st.header("Input settings")
    n = st.slider("Number of cities", 3, 16, 9)
    seed = st.number_input("Random seed", min_value=0, max_value=999999, value=42, step=1)
    start = st.selectbox("Starting city", options=list(range(n)), index=0)
    st.caption("Exact algorithms are expensive. Brute Force and Branch and Bound use an 8-second safety limit.")
    selected = st.multiselect("Algorithms to run", ALGORITHMS, default=ALGORITHMS[:4])
    run_button = st.button("Run comparison", type="primary", use_container_width=True)

points = make_cities(n, int(seed))
d = distances_from_points(points)
if "results" not in st.session_state:
    st.session_state.results = None
if run_button:
    if not selected:
        st.warning("Select at least one algorithm.")
    else:
        results = []
        progress = st.progress(0)
        for idx, name in enumerate(selected):
            results.append(run_algorithm(name, d, start))
            progress.progress((idx + 1) / len(selected))
        st.session_state.results = results
        progress.empty()

left, right = st.columns([1.2, 1])
with left:
    st.subheader("City map")
    fig, ax = plt.subplots(figsize=(7, 5))
    xs, ys = zip(*points)
    ax.scatter(xs, ys)
    for i, (x, y) in enumerate(points):
        ax.annotate(str(i), (x, y), xytext=(5, 5), textcoords="offset points")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Generated city coordinates")
    ax.grid(alpha=0.25)
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Distance matrix")
    st.dataframe(pd.DataFrame(d, columns=[f"City {i}" for i in range(n)],
                              index=[f"City {i}" for i in range(n)]).round(1),
                 use_container_width=True, height=340)

if st.session_state.results:
    st.divider()
    st.subheader("Results")
    rows = []
    for r in st.session_state.results:
        rows.append({k: r[k] for k in ["Algorithm", "Distance", "Time (ms)", "Completed", "States / tours checked"]})
    result_df = pd.DataFrame(rows)
    exact_completed = [r["Distance"] for r in st.session_state.results
                       if r["Algorithm"] in ["Held–Karp DP", "Branch and Bound", "Brute Force"] and r["Completed"]]
    optimum = min(exact_completed) if exact_completed else None
    if optimum is not None and optimum > 0:
        result_df["Gap vs best completed exact (%)"] = result_df["Distance"].apply(lambda x: 100 * (x - optimum) / optimum)
    st.dataframe(result_df.round(3), use_container_width=True)
    st.caption("A timed-out exact search returns its best tour found so far; it is not proven optimal. The gap uses the best completed exact result available in this run.")
    best = min(st.session_state.results, key=lambda x: x["Distance"])
    st.metric("Shortest tour found", f"{best['Distance']:.2f}", best["Algorithm"])
    st.subheader(f"Route: {best['Algorithm']}")
    route = best["Tour"]
    closed = route + [route[0]]
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(xs, ys)
    for i, (x, y) in enumerate(points):
        ax2.annotate(str(i), (x, y), xytext=(5, 5), textcoords="offset points")
    for a, b in zip(closed[:-1], closed[1:]):
        ax2.annotate("", xy=points[b], xytext=points[a],
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.08"))
    ax2.set_title(" → ".join(map(str, route)) + f" → {route[0]}")
    ax2.grid(alpha=0.25)
    st.pyplot(fig2)
    plt.close(fig2)
    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download comparison CSV", csv, "tsp_comparison.csv", "text/csv")
else:
    st.info("Choose algorithms in the sidebar and click **Run comparison** to generate routes and benchmark results.")

with st.expander("Algorithm notes and complexity"):
    st.markdown("""
    - **Brute Force:** checks all `(n−1)!` tours with a fixed starting city. Time: `O(n!)`.
    - **Held–Karp DP:** dynamic programming over subsets. Time: `O(n² 2ⁿ)`; space: `O(n 2ⁿ)`.
    - **Branch and Bound:** exact when it finishes; uses an MST-based lower bound to prune branches. Worst case is exponential.
    - **Nearest Neighbour:** greedily visits the nearest unvisited city. Time: `O(n²)`; no general optimality guarantee.
    - **MST 2-Approximation:** takes a preorder traversal of a minimum spanning tree. Time: `O(n²)` for this dense graph implementation; at most twice optimal for metric TSP.
    """)
