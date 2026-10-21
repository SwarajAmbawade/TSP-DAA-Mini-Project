# Mini Project Report Template

## Title
Comparative Analysis of Exact and Approximation Algorithms for the Travelling Salesperson Problem

## Abstract
The Travelling Salesperson Problem (TSP) asks for a minimum-cost Hamiltonian cycle in a weighted graph. This project implements and compares three exact methods—Brute Force, Held–Karp Dynamic Programming, and Branch and Bound—with Nearest Neighbour and an MST-based 2-approximation for metric TSP. The application visualizes routes and records execution time and tour cost across generated Euclidean instances. Results should be filled using measurements obtained from the student's own runs.

## 1. Problem Statement
Given n cities and pairwise travel costs, find a minimum-cost closed tour that visits each city exactly once and returns to the starting city.

## 2. Objectives
- Implement exact and approximation/heuristic TSP algorithms.
- Compare solution costs and runtime.
- Observe how runtime scales as city count increases.
- Visualize the resulting tours and export benchmark data.

## 3. Algorithm Summary
### Brute Force
Fix one city as the start, enumerate every permutation of the remaining cities, calculate each tour cost, and keep the minimum. Time complexity: O(n!).

### Held–Karp Dynamic Programming
Use subset states to store the minimum cost of reaching each last city after visiting a subset. Time complexity: O(n² 2ⁿ); space complexity: O(n 2ⁿ).

### Branch and Bound
Explore partial tours, maintaining the best complete tour found. Prune a partial tour when a valid lower bound on any completion is no better than the current best. Worst-case time is exponential; the algorithm is exact if it completes.

### Nearest Neighbour
From the current city, choose the nearest unvisited city until all cities are visited, then return to the start. Time complexity: O(n²). It is a heuristic and has no general optimality guarantee.

### MST 2-Approximation
Build a minimum spanning tree and visit vertices in preorder, shortcutting repeated vertices. For metric TSP, the resulting tour costs at most twice the optimal tour. This guarantee does not hold for arbitrary non-metric cost matrices.

## 4. Experimental Method
Use the same generated point sets and starting city for each algorithm. Run several random seeds and record:
- Number of cities
- Algorithm
- Tour distance
- Runtime in milliseconds
- Whether an exact search completed
- Approximation gap relative to a completed exact optimum

## 5. Results
Insert exported CSV tables and charts here. Do not invent results. State the hardware and Python version used.

## 6. Discussion
Discuss the runtime growth of exact algorithms, the quality of heuristic solutions, and the effect of Branch and Bound pruning. Explain that timings are machine-dependent and that a timed-out exact search has not proven optimality.

## 7. Conclusion
Complete after running experiments. Summarize which methods were practical at each tested input size and whether approximate methods provided acceptable tour quality.

## 8. Future Scope
- Add user-entered distance matrices.
- Compare multiple starting cities for Nearest Neighbour.
- Add 2-opt local improvement.
- Add repeated benchmark trials and runtime plots.
- Add real road-network distance data.
