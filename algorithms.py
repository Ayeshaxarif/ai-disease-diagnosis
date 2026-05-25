from collections import deque
from knowledge_base import diseases

# ── BFS ──────────────────────────────────────────
def bfs_diagnose(user_symptoms, age_group="adult"):
    queue = deque(list(diseases.keys()))
    matches = []
    print("BFS Traversal:")
    while queue:
        disease = queue.popleft()
        d_symptoms = diseases[disease]["symptoms"]
        common = set(user_symptoms) & set(d_symptoms.keys())
        if common:
            # Weighted score — symptom ka weight bhi count ho
            weighted_score = sum(d_symptoms[s] for s in common)
            print(f"  {disease} -> matched: {len(common)} symptoms, weight: {weighted_score}")
            if len(common) >= 2:
                matches.append((disease, weighted_score))
    return sorted(matches, key=lambda x: x[1], reverse=True)

# ── GBFS ─────────────────────────────────────────
def gbfs_diagnose(user_symptoms, age_group="adult"):
    scored = []
    for disease, info in diseases.items():
        d_symptoms = info["symptoms"]
        common = set(user_symptoms) & set(d_symptoms.keys())
        if common:
            weighted = sum(d_symptoms[s] for s in common)
            total_weight = sum(d_symptoms.values())
            heuristic = weighted / total_weight
            scored.append((disease, heuristic))
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    print("\nGBFS Traversal (Greedy Best First):")
    for disease, score in scored[:5]:
        print(f"  {disease} -> heuristic: {score:.2f}")
    if not scored:
        return "No match", 0
    return scored[0][0], scored[0][1]

# ── A* ───────────────────────────────────────────
def astar_path(user_symptoms, age_group="adult"):
    print("\nA* Path Finding:")
    best, best_score = None, 0
    for disease, info in diseases.items():
        d_symptoms = info["symptoms"]
        common = set(user_symptoms) & set(d_symptoms.keys())
        if common:
            g_cost = sum(d_symptoms[s] for s in common)
            total = sum(d_symptoms.values())
            h_cost = g_cost / total
            f_cost = g_cost + h_cost
            print(f"  {disease} -> g:{g_cost} h:{h_cost:.2f} f:{f_cost:.2f}")
            if f_cost > best_score:
                best_score = f_cost
                best = disease
    return best, best_score

# ── MINIMAX ──────────────────────────────────────
def minimax_decision(candidates):
    print("\nMinimax Decision:")
    if not candidates:
        return "No match found"
    for d, s in candidates:
        print(f"  {d} -> weighted score: {s}")
    best = max(candidates, key=lambda x: x[1])[0]
    print(f"Final Decision: {best}")
    return best

# ── RISK ASSESSMENT ──────────────────────────────
def get_risk_assessment(disease, age_group="adult"):
    info = diseases.get(disease, {})
    base_risk = info.get("risk_level", "UNKNOWN")
    age_risk = info.get("age_risk", {}).get(age_group, "UNKNOWN")
    treatment = info.get("treatment", "Consult a doctor")
    return {
        "disease": disease,
        "base_risk": base_risk,
        "age_risk": age_risk,
        "treatment": treatment
    }

# ── MULTIPLE DISEASE WARNING ──────────────────────
def check_overlapping_diseases(candidates):
    if len(candidates) >= 2:
        top_two = candidates[:2]
        if abs(top_two[0][1] - top_two[1][1]) <= 2:
            print(f"\n⚠️  WARNING: Symptoms overlap!")
            print(f"   Both {top_two[0][0]} and {top_two[1][0]} are possible!")
            return True
    return False

print("Upgraded Algorithms loaded!")
print("Features: Weighted BFS + GBFS + A* + Minimax + Risk Assessment + Overlap Warning!")
