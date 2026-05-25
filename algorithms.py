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
            weighted_score = sum(d_symptoms[s] for s in common)
            print(f"  {disease} -> matched: {len(common)}, weight: {weighted_score}")
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
    print("\nGBFS Traversal:")
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

# ── DIFFERENTIAL DIAGNOSIS ───────────────────────
def differential_diagnosis(user_symptoms, age_group="adult"):
    all_scores = []
    for disease, info in diseases.items():
        d_symptoms = info["symptoms"]
        common = set(user_symptoms) & set(d_symptoms.keys())
        if common:
            weighted = sum(d_symptoms[s] for s in common)
            total = sum(d_symptoms.values())
            probability = round((weighted / total) * 100, 1)
            all_scores.append((disease, probability))
    all_scores = sorted(all_scores, key=lambda x: x[1], reverse=True)
    top3 = all_scores[:3]
    print("\nDifferential Diagnosis (Top 3):")
    for disease, prob in top3:
        print(f"  {disease} -> {prob}% probability")
    return top3

# ── SYMPTOM SEVERITY ─────────────────────────────
def calculate_severity(user_symptoms, severity_levels):
    # severity_levels = {"fever": "severe", "cough": "mild"}
    severity_score = 0
    for symptom in user_symptoms:
        level = severity_levels.get(symptom, "mild")
        if level == "mild":
            severity_score += 1
        elif level == "moderate":
            severity_score += 2
        elif level == "severe":
            severity_score += 3
    if severity_score <= 3:
        return "MILD", severity_score
    elif severity_score <= 7:
        return "MODERATE", severity_score
    else:
        return "SEVERE", severity_score

# ── EMERGENCY ALERT ──────────────────────────────
def check_emergency(disease, user_symptoms):
    info = diseases.get(disease, {})
    emergency_symptoms = info.get("emergency_symptoms", [])
    triggered = set(user_symptoms) & set(emergency_symptoms)
    if triggered or info.get("risk_level") == "CRITICAL":
        print(f"\n🚨 EMERGENCY ALERT!")
        print(f"   Go to hospital immediately!")
        print(f"   Dangerous symptoms: {triggered if triggered else 'Critical disease detected'}")
        return True
    return False

# ── MEDICINE INTERACTION ─────────────────────────
def check_medicine_interaction(disease, current_medicines):
    info = diseases.get(disease, {})
    recommended = info.get("medicines", [])
    conflicts = []
    safe = []
    dangerous_combos = {
        ("ibuprofen", "aspirin"): "Increases bleeding risk",
        ("paracetamol", "alcohol"): "Liver damage risk",
        ("metformin", "alcohol"): "Dangerous blood sugar drop",
        ("warfarin", "ibuprofen"): "Severe bleeding risk",
        ("ciprofloxacin", "antacid"): "Reduces antibiotic effectiveness",
    }
    for med in current_medicines:
        for rec in recommended:
            pair = tuple(sorted([med.lower(), rec.lower()]))
            if pair in dangerous_combos:
                conflicts.append(f"{med} + {rec}: {dangerous_combos[pair]}")
    return recommended, conflicts

# ── PATIENT HISTORY ──────────────────────────────
patient_history = {}

def save_patient_history(patient_id, symptoms, diagnosis, age_group):
    if patient_id not in patient_history:
        patient_history[patient_id] = []
    patient_history[patient_id].append({
        "symptoms": symptoms,
        "diagnosis": diagnosis,
        "age_group": age_group,
    })
    print(f"\nPatient history saved! Total visits: {len(patient_history[patient_id])}")

def get_patient_history(patient_id):
    history = patient_history.get(patient_id, [])
    if not history:
        print("No history found for this patient.")
        return []
    print(f"\nPatient History ({len(history)} visits):")
    for i, visit in enumerate(history, 1):
        print(f"  Visit {i}: {visit['diagnosis']} | Symptoms: {visit['symptoms']}")
    # Check chronic risk
    diagnoses = [v["diagnosis"] for v in history]
    if len(set(diagnoses)) == 1 and len(diagnoses) >= 2:
        disease = diagnoses[0]
        chronic = diseases.get(disease, {}).get("chronic_risk", "LOW")
        print(f"  ⚠️  Same disease repeated! Chronic Risk: {chronic}")
    return history

# ── RISK ASSESSMENT ──────────────────────────────
def get_risk_assessment(disease, age_group="adult"):
    info = diseases.get(disease, {})
    return {
        "disease": disease,
        "base_risk": info.get("risk_level", "UNKNOWN"),
        "age_risk": info.get("age_risk", {}).get(age_group, "UNKNOWN"),
        "treatment": info.get("treatment", "Consult a doctor"),
        "chronic_risk": info.get("chronic_risk", "LOW"),
        "medicines": info.get("medicines", []),
    }

# ── OVERLAP WARNING ──────────────────────────────
def check_overlapping_diseases(candidates):
    if len(candidates) >= 2:
        top_two = candidates[:2]
        if abs(top_two[0][1] - top_two[1][1]) <= 2:
            print(f"\n⚠️  WARNING: Symptoms overlap!")
            print(f"   Both {top_two[0][0]} and {top_two[1][0]} are possible!")
            return True
    return False

print("Advanced Algorithms loaded!")
print("BFS + GBFS + A* + Minimax + Differential Diagnosis")
print("Severity + Emergency Alert + Medicine Interaction + Patient History!")
