from collections import deque
from knowledge_base import diseases

def bfs_diagnose(user_symptoms):
    queue = deque(list(diseases.keys()))
    matches = []
    print("BFS Traversal:")
    while queue:
        disease = queue.popleft()
        common = set(user_symptoms) & set(diseases[disease]["symptoms"])
        print(f"  Checking: {disease} -> matched: {len(common)}")
        if len(common) >= 2:
            matches.append((disease, len(common)))
    return sorted(matches, key=lambda x: x[1], reverse=True)

def gbfs_diagnose(user_symptoms):
    scored = []
    for disease, info in diseases.items():
        matched = len(set(user_symptoms) & set(info["symptoms"]))
        heuristic = matched / len(info["symptoms"])
        scored.append((disease, heuristic))
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    print("\nGBFS Traversal:")
    for disease, score in scored[:5]:
        print(f"  {disease} -> heuristic: {score:.2f}")
    return scored[0][0], scored[0][1]

def astar_path(user_symptoms):
    print("\nA* Path Finding:")
    best, best_score = None, 0
    for disease, info in diseases.items():
        matched = len(set(user_symptoms) & set(info["symptoms"]))
        heuristic = matched / len(info["symptoms"])
        f_cost = matched + heuristic
        print(f"  {disease} -> f_cost: {f_cost:.2f}")
        if f_cost > best_score:
            best_score = f_cost
            best = disease
    return best, best_score

def minimax_decision(candidates):
    print("\nMinimax Decision:")
    if not candidates:
        return "No match found"
    for d, s in candidates:
        print(f"  {d} -> score: {s}")
    best = max(candidates, key=lambda x: x[1])[0]
    print(f"Final: {best}")
    return best

print("Algorithms ready! BFS + GBFS + A* + Minimax loaded!")
