import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

# Importing Member 1's Advanced Backend Algorithms
from algorithms import (bfs_diagnose, gbfs_diagnose, astar_path,
                        minimax_decision, differential_diagnosis, calculate_severity,
                        check_emergency, check_medicine_interaction,
                        save_patient_history, get_patient_history,
                        get_risk_assessment, check_overlapping_diseases)

# Importing Member 2's Machine Learning Models
from ml_models import predict_all, get_confusion_matrix, get_model_accuracy

# Importing Member 1's LLM components and Member 3's Voice Engine
from groq_diagnosis import get_diagnosis_explanation, get_overlap_explanation
from voice_output import speak

st.set_page_config(page_title="AI Disease Diagnosis", layout="wide")
st.title("AI Disease Diagnosis System")

with st.sidebar:
    st.header("Settings")
    patient_id = st.text_input("Patient ID", value="P001")
    age_group = st.selectbox("Age Group", ["child", "adult", "elderly"])
    voice_on = st.toggle("Voice Output", value=True)
    show_cm = st.checkbox("Show Confusion Matrix")
    show_hist = st.checkbox("Show Patient History")

all_symp = ["fever", "cough", "fatigue", "thirst", "chills",
            "stomach_pain", "shortness_of_breath", "headache",
            "loss of smell", "joint pain", "rash", "nausea", "dizziness"]

st.subheader("Step 1: Select Symptoms")
selected = st.multiselect("Choose all that apply:", all_symp)

sev_levels = {}
if selected:
    st.subheader("Step 2: Rate Severity")
    cols = st.columns(3)
    for i, s in enumerate(selected):
        with cols[i % 3]:
            sev_levels[s] = st.select_slider(f"Severity for {s}", ["mild", "moderate", "severe"])
            
    cur_meds = st.text_input("Current medicines (comma separated):", "")
    cur_meds_list = [m.strip() for m in cur_meds.split(",") if m.strip()]

if st.button("Diagnose Now", type="primary") and selected:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Algorithm Results")
        bfs_r = bfs_diagnose(selected, age_group)
        final = minimax_decision(bfs_r) if bfs_r else "Unknown"
        gs = gbfs_diagnose(selected, age_group)
        ar = astar_path(selected, age_group)
        top3 = differential_diagnosis(selected, age_group)
        sev, sc = calculate_severity(selected, sev_levels)
        
        st.success(f"BFS + Minimax Diagnosis: {final}")
        st.info(f"A* Best Match: {ar}")
        st.info(f"GBFS Confidence: {gs[1]:.0%}")
        st.warning(f"Severity: {sev} (score: {sc})")
        
        st.write("**Top 3 Differential Diagnosis:**")
        for d, p in top3:
            st.write(f"- {d}: {p}%")
            
    with col2:
        st.subheader("ML Model Results")
        ml_symptoms = ["fever", "cough", "fatigue", "thirst", "chills", "stomach_pain", "shortness_of_breath", "headache"]
        sd = {s: 1 if s in selected else 0 for s in ml_symptoms}
        
        ml_r = predict_all(sd)
        acc = get_model_accuracy()
        
        for m, r in ml_r.items():
            st.success(f"{m}: {r} (accuracy: {acc[m]}%)")
            
        if show_cm:
            st.subheader("Confusion Matrix")
            st.dataframe(get_confusion_matrix("knn"))
            
    risk = get_risk_assessment(final, age_group)
    if check_emergency(final, selected):
        st.error("EMERGENCY! Go to hospital immediately!")
        
    overlap = check_overlapping_diseases(bfs_r)
    rec, conflicts = check_medicine_interaction(final, cur_meds_list)
    if conflicts:
        st.error(f"Medicine Conflict Detected: {conflicts}")
        
    save_patient_history(patient_id, selected, final, age_group)
    
    if show_hist:
        st.subheader("Patient History")
        st.write(get_patient_history(patient_id))
        
    st.subheader("AI Explanation")
    exp = get_diagnosis_explanation(final, selected, risk["base_risk"], age_group)
    st.write(exp)
    
    if overlap and len(bfs_r) >= 2:
        st.subheader("Overlap Analysis")
        st.write(get_overlap_explanation(bfs_r[0][0], bfs_r[1][0], selected))
        
    if voice_on:
        audio = speak(f"Diagnosis complete. You likely have {final}. Risk level is {risk['base_risk']}.")
        st.audio(audio, format="audio/mp3")
        
    st.subheader("Final Report")
    st.json({
        "Patient ID": patient_id,
        "Diagnosis": final,
        "Severity": sev,
        "Base Risk": risk["base_risk"],
        "Age Risk": risk["age_risk"],
        "Chronic Risk": risk["chronic_risk"],
        "Treatment": risk["treatment"],
        "Recommended Meds": rec,
        "Medicine Conflicts": conflicts,
    })