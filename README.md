# TSP Algorithm Lab — DAA Mini Project

## Project title
**Comparative Analysis of Exact and Approximation Algorithms for the Travelling Salesperson Problem**

## Included algorithms
1. Brute Force (exact)
2. Held–Karp Dynamic Programming (exact)
3. Branch and Bound (exact when it completes)
4. Nearest Neighbour (heuristic)
5. MST preorder 2-Approximation (approximation for metric TSP)

## Requirements
- Python 3.10+
- Packages listed in `requirements.txt`

## Run on Windows
1. Extract the ZIP.
2. Open the extracted folder in VS Code or PowerShell.
3. Create a virtual environment (recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   streamlit run app.py
   ```
6. Open the local URL printed in the terminal (usually http://localhost:8501).

## How to use
- Set the number of cities and random seed in the sidebar.
- Select algorithms and click **Run comparison**.
- Compare tour distance, runtime, completion status, and search counts.
- Download results as CSV.
- The app shows the generated cities, distance matrix, and best tour found.

## Important interpretation notes
- City labels start at 0.
- All generated distances are Euclidean, symmetric, and satisfy the triangle inequality.
- The MST-based 2-approximation guarantee only applies to metric TSP.
- Brute Force and Branch and Bound have an 8-second limit in this demo. If a search times out, its returned route is the best route it found so far and is **not proven optimal**.
- Held–Karp is exponential too. Keep city counts modest (roughly 15 or fewer for a responsive demo, depending on machine).
- Benchmark timings vary by machine and load. Record your own measured results; do not copy made-up results into the report.

## Suggested report structure
1. Abstract
2. Introduction and TSP problem statement
3. Objectives and scope
4. Theory and pseudocode for each algorithm
5. System design / flowchart
6. Implementation details
7. Test cases and experimental setup
8. Results table and graphs
9. Complexity comparison
10. Conclusion and future scope

## Suggested test cases
- 5–8 cities: run all algorithms and compare exact optimum with approximate routes.
- 9–12 cities: compare Held–Karp, Branch and Bound, Nearest Neighbour, and MST approximation.
- 13–16 cities: focus on the two practical algorithms and Held–Karp if runtime allows.
- Repeat with several random seeds for more defensible results.

## Result
1. Input settings :
   <img width="1920" height="1080" alt="Screenshot 2026-10-21 141343" src="https://github.com/user-attachments/assets/fc0e9163-7f15-4883-b9c5-481400ea2f1c" />

2. Result :
   <img width="1920" height="1080" alt="Screenshot 2026-10-21 141422" src="https://github.com/user-attachments/assets/65025d78-f481-48b5-b40f-ef95351c3421" />

3. Graph :
   <img width="1920" height="1080" alt="Screenshot 2026-10-21 141456" src="https://github.com/user-attachments/assets/68fba4dc-a855-4dc2-ae00-f67e075453d3" />


## Complexity summary
| Algorithm | Time complexity | Optimal? |
|---|---|---|
| Brute Force | O(n!) | Yes, if completed |
| Held–Karp DP | O(n² 2ⁿ) | Yes |
| Branch and Bound | Exponential worst case | Yes, if completed |
| Nearest Neighbour | O(n²) | No guarantee |
| MST 2-Approximation | O(n²) in this implementation | ≤ 2× optimum for metric TSP |

## Limitations
- This is a teaching/benchmark application, not a production route planner.
- Instances are generated as Euclidean points; there is no road-network traffic data.
- Runtime comparisons should use the same machine and repeat runs for consistency.
