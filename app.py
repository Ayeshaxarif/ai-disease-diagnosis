import streamlit as st
import os
from dotenv import load_dotenv
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

try:
    from algorithms import (bfs_diagnose, gbfs_diagnose, astar_path,
        minimax_decision, differential_diagnosis, calculate_severity,
        check_emergency, check_medicine_interaction,
        save_patient_history, get_patient_history,
        get_risk_assessment, check_overlapping_diseases)
    from ml_models import predict_all, get_confusion_matrix, get_model_accuracy
    from groq_diagnosis import get_diagnosis_explanation, get_overlap_explanation
    from voice_output import speak
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False

st.set_page_config(
    page_title="MediAI - Smart Disease Diagnosis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }

    /* ===== LIGHT BLUE THEME ===== */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 40%, #dbeafe 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f9ff 100%);
        border-right: 1px solid #bae6fd;
    }

    [data-testid="stSidebar"] .stMarkdown { color: #0f172a; }
    [data-testid="stSidebar"] p { color: #475569; }
    [data-testid="stSidebar"] h1 { color: #0369a1 !important; }
    [data-testid="stSidebar"] h2 { color: #0c4a6e !important; border-color: #38bdf8 !important; }
    [data-testid="stSidebar"] h3 { color: #334155 !important; }

    /* Main text colors */
    h1 {
        background: linear-gradient(90deg, #0284c7, #6366f1, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        animation: fadeInDown 0.8s ease-out;
    }

    h2 {
        color: #0f172a !important;
        font-weight: 700 !important;
        border-left: 4px solid #0284c7;
        padding-left: 15px;
        margin-top: 2rem !important;
        animation: slideInLeft 0.6s ease-out;
    }

    h3 { color: #334155 !important; font-weight: 600 !important; }
    p { color: #475569; }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(2, 132, 199, 0.2); }
        50% { box-shadow: 0 0 30px rgba(2, 132, 199, 0.5); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    @keyframes progressFill {
        from { width: 0; }
    }

    .animate-fadeInUp { animation: fadeInUp 0.6s ease-out forwards; }
    .animate-fadeIn { animation: fadeIn 0.5s ease-out forwards; }
    .animate-slideInLeft { animation: slideInLeft 0.5s ease-out forwards; }
    .animate-slideInRight { animation: slideInRight 0.5s ease-out forwards; }
    .animate-scaleIn { animation: scaleIn 0.4s ease-out forwards; }

    /* Delay classes */
    .delay-1 { animation-delay: 0.1s; opacity: 0; }
    .delay-2 { animation-delay: 0.2s; opacity: 0; }
    .delay-3 { animation-delay: 0.3s; opacity: 0; }
    .delay-4 { animation-delay: 0.4s; opacity: 0; }
    .delay-5 { animation-delay: 0.5s; opacity: 0; }

    /* ===== CARDS - LIGHT THEME ===== */
    .symptom-card {
        background: linear-gradient(145deg, #ffffff, #f0f9ff);
        border: 2px solid #e0f2fe;
        border-radius: 16px;
        padding: 18px 10px;
        margin: 8px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.08);
        animation: fadeInUp 0.5s ease-out forwards;
        opacity: 0;
    }
    .symptom-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #38bdf8;
        box-shadow: 0 12px 30px rgba(2, 132, 199, 0.2);
    }
    .symptom-card.selected {
        background: linear-gradient(145deg, #e0f2fe, #bae6fd);
        border-color: #0284c7;
        box-shadow: 0 0 25px rgba(2, 132, 199, 0.3);
        animation: pulseGlow 2s infinite;
    }

    .result-card {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(2, 132, 199, 0.12);
    }

    .diagnosis-main {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        border: 2px solid #38bdf8;
        border-radius: 24px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 10px 50px rgba(2, 132, 199, 0.3);
        animation: scaleIn 0.7s ease-out, pulseGlow 3s infinite;
        color: white;
    }

    /* ===== PROGRESS STEPS ===== */
        .step-container {
        display: none;
        animation: fadeInUp 0.5s ease-out;
    }
    .step {
        width: 55px;
        height: 55px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.3rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .step-active {
        background: linear-gradient(135deg, #38bdf8, #6366f1);
        color: white;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.5);
        animation: float 3s ease-in-out infinite;
    }
    .step-completed {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        animation: scaleIn 0.4s ease-out;
    }
    .step-pending {
        background: #e2e8f0;
        color: #94a3b8;
    }
    .step-line {
        width: 90px;
        height: 4px;
        background: #e2e8f0;
        margin: 0 12px;
        border-radius: 2px;
        overflow: hidden;
    }
    .step-line-completed {
        background: linear-gradient(90deg, #10b981, #38bdf8);
        animation: progressFill 0.8s ease-out forwards;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #0284c7, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 45px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.35) !important;
        animation: fadeInUp 0.5s ease-out;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(2, 132, 199, 0.5) !important;
    }
    .stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f0f9ff);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e0f2fe;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.08);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out forwards;
        opacity: 0;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.15);
        border-color: #38bdf8;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0284c7, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label { color: #64748b; font-size: 0.9rem; margin-top: 5px; }

    /* ===== EMERGENCY ALERT ===== */
    .emergency-alert {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 2px solid #f87171;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        animation: pulseGlow 2s infinite, fadeInUp 0.5s ease-out;
        margin: 20px 0;
    }

    /* ===== PILLS / TAGS ===== */
    .pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
        animation: scaleIn 0.3s ease-out forwards;
        opacity: 0;
    }
    .pill-symptom {
        background: rgba(2, 132, 199, 0.1);
        color: #0284c7;
        border: 1px solid rgba(2, 132, 199, 0.2);
    }
    .pill-disease {
        background: rgba(99, 102, 241, 0.1);
        color: #6366f1;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }

    /* ===== DIVIDER ===== */
    .fancy-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #38bdf8, #6366f1, transparent);
        margin: 35px 0;
        border: none;
        border-radius: 2px;
        animation: fadeIn 1s ease-out;
    }

    /* ===== CHART CONTAINER ===== */
    .chart-container {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
    }

    /* ===== LOADING SPINNER ===== */
    .loading-spinner {
        border: 4px solid #e0f2fe;
        border-top: 4px solid #0284c7;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 30px auto;
    }

    /* ===== INFO BOXES ===== */
    .info-box {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border-left: 4px solid #0284c7;
        border-radius: 12px;
        padding: 15px 20px;
        margin: 10px 0;
        animation: slideInLeft 0.5s ease-out forwards;
        opacity: 0;
    }

    /* ===== RISK BADGES ===== */
    .risk-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.95rem;
        animation: scaleIn 0.4s ease-out;
    }
    .risk-low { background: rgba(16, 185, 129, 0.15); color: #059669; border: 1px solid rgba(16, 185, 129, 0.3); }
    .risk-medium { background: rgba(245, 158, 11, 0.15); color: #d97706; border: 1px solid rgba(245, 158, 11, 0.3); }
    .risk-high { background: rgba(249, 115, 22, 0.15); color: #ea580c; border: 1px solid rgba(249, 115, 22, 0.3); }
    .risk-critical { background: rgba(239, 68, 68, 0.15); color: #dc2626; border: 1px solid rgba(239, 68, 68, 0.3); }

    /* ===== HIDE DEFAULT ELEMENTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #f0f9ff; }
    ::-webkit-scrollbar-thumb { background: #bae6fd; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #7dd3fc; }

    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #e0f2fe !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2) !important;
    }

    /* ===== SELECT BOX ===== */
    .stSelectbox > div > div > div {
        background: white !important;
        border: 2px solid #e0f2fe !important;
        border-radius: 12px !important;
        color: #0f172a !important;
    }

    /* ===== TOGGLE ===== */
    .stToggle > div > div > div {
        background: #e0f2fe !important;
    }

    /* ===== ANIMATED BAR (for differential) ===== */
    .animated-bar-bg {
        flex: 1;
        background: #e2e8f0;
        height: 24px;
        border-radius: 12px;
        overflow: hidden;
        position: relative;
    }
    .animated-bar-fill {
        height: 100%;
        border-radius: 12px;
        animation: progressFill 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        position: relative;
        overflow: hidden;
    }
    .animated-bar-fill::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
        background-size: 200% 100%;
    }
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []
if 'severity_levels' not in st.session_state:
    st.session_state.severity_levels = {}
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = "P001"
if 'age_group' not in st.session_state:
    st.session_state.age_group = "adult"
if 'diagnosis_results' not in st.session_state:
    st.session_state.diagnosis_results = None

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 25px 0; animation: fadeInUp 0.5s ease-out;">
        <div style="font-size: 3.5rem; animation: float 3s ease-in-out infinite;">🏥</div>
        <h2 style="color: #0284c7; margin: 12px 0; border: none; padding: 0; font-size: 1.5rem;">MediAI</h2>
        <p style="color: #64748b; font-size: 0.95rem;">Smart Disease Diagnosis</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #e0f2fe; margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #0f172a;'>👤 Patient Information</h3>", unsafe_allow_html=True)
    st.session_state.patient_id = st.text_input(
        "Patient ID", 
        value=st.session_state.patient_id,
        help="Enter unique patient identifier"
    )

    st.session_state.age_group = st.selectbox(
        "Age Group",
        ["child", "adult", "elderly"],
        index=["child", "adult", "elderly"].index(st.session_state.age_group),
        help="Select patient's age group for risk assessment"
    )

    st.markdown("<hr style='border-color: #e0f2fe; margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #0f172a;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    voice_on = st.toggle("🔊 Voice Output", value=True)
    show_cm = st.checkbox("📊 Show Confusion Matrix")
    show_hist = st.checkbox("📋 Show Patient History")
    show_charts = st.checkbox("📈 Show Charts & Graphs", value=True)

    st.markdown("<hr style='border-color: #e0f2fe; margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #0f172a;'>📈 System Stats</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="metric-card delay-1">
            <div class="metric-value">20+</div>
            <div class="metric-label">Diseases</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card delay-2">
            <div class="metric-value">5</div>
            <div class="metric-label">AI Models</div>
        </div>
        """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
        <div class="metric-card delay-3">
            <div class="metric-value">4</div>
            <div class="metric-label">Algorithms</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-card delay-4">
            <div class="metric-value">AI</div>
            <div class="metric-label">Powered</div>
        </div>
        """, unsafe_allow_html=True)

# ===== MAIN CONTENT =====
st.markdown("""
<div style="text-align: center; padding: 25px 0;">
    <h1>MediAI Diagnosis System</h1>
</div>
""", unsafe_allow_html=True)

# Progress Steps
step1_class = "step-completed" if st.session_state.page in ['severity', 'results'] else "step-active" if st.session_state.page == 'input' else "step-pending"
step2_class = "step-completed" if st.session_state.page == 'results' else "step-active" if st.session_state.page == 'severity' else "step-pending"
step3_class = "step-active" if st.session_state.page == 'results' else "step-pending"
line1_class = "step-line-completed" if st.session_state.page in ['severity', 'results'] else ""
line2_class = "step-line-completed" if st.session_state.page == 'results' else ""

st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: center; margin: 10px 0 25px 0; padding: 15px 30px; background: linear-gradient(135deg, #ffffff, #f0f9ff); border-radius: 50px; border: 2px solid #e0f2fe; box-shadow: 0 4px 20px rgba(2, 132, 199, 0.1); width: fit-content; margin-left: auto; margin-right: auto; animation: fadeInUp 0.6s ease-out;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <div class="step {step1_class}" style="width: 42px; height: 42px; font-size: 1rem;">1</div>
            <span style="color: #475569; font-size: 0.8rem; font-weight: 600;">Symptoms</span>
        </div>
        <div class="step-line {line1_class}" style="width: 50px; margin: 0;"></div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <div class="step {step2_class}" style="width: 42px; height: 42px; font-size: 1rem;">2</div>
            <span style="color: #475569; font-size: 0.8rem; font-weight: 600;">Severity</span>
        </div>
        <div class="step-line {line2_class}" style="width: 50px; margin: 0;"></div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <div class="step {step3_class}" style="width: 42px; height: 42px; font-size: 1rem;">3</div>
            <span style="color: #475569; font-size: 0.8rem; font-weight: 600;">Diagnosis</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

# ===== PAGE 1: SYMPTOM SELECTION =====
if st.session_state.page == 'input':
    st.markdown("""
    <h2>🩺 Step 1: Select Your Symptoms</h2>
    <p style="color: #475569; font-size: 1.05rem;">Click on the symptoms you are experiencing. You can select multiple symptoms.</p>
    """, unsafe_allow_html=True)

    all_symptoms = [
        ("🤒", "fever", "Elevated body temperature"),
        ("🤧", "cough", "Persistent coughing"),
        ("😴", "fatigue", "Extreme tiredness"),
        ("🥤", "thirst", "Excessive thirst"),
        ("🥶", "chills", "Feeling cold/shivering"),
        ("🤢", "stomach_pain", "Abdominal discomfort"),
        ("😮‍💨", "shortness_of_breath", "Difficulty breathing"),
        ("🤕", "headache", "Head pain/pressure"),
        ("👃", "loss of smell", "Anosmia"),
        ("🦴", "joint pain", "Joint discomfort"),
        ("🔴", "rash", "Skin irritation"),
        ("🤮", "nausea", "Feeling sick"),
        ("😵‍💫", "dizziness", "Lightheadedness"),
    ]

    cols = st.columns(4)
    for i, (emoji, symptom, desc) in enumerate(all_symptoms):
        with cols[i % 4]:
            is_selected = symptom in st.session_state.selected_symptoms
            delay_class = f"delay-{min(i+1, 5)}"

            if st.button(
                f"{emoji} {symptom.replace('_', ' ').title()}",
                key=f"symptom_{symptom}",
                use_container_width=True,
                help=desc
            ):
                if is_selected:
                    st.session_state.selected_symptoms.remove(symptom)
                else:
                    st.session_state.selected_symptoms.append(symptom)
                st.rerun()

            st.markdown(f"""
            <div style="text-align: center; color: #64748b; font-size: 0.78rem; margin-top: -6px; margin-bottom: 12px;" class="animate-fadeIn {delay_class}">
                {desc}
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.selected_symptoms:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0f172a;'>✅ Selected Symptoms</h3>", unsafe_allow_html=True)
        pills_html = ""
        for idx, s in enumerate(st.session_state.selected_symptoms):
            pills_html += f'<span class="pill pill-symptom" style="animation-delay: {idx*0.1}s">{s.replace("_", " ").title()}</span>'
        st.markdown(f"""
        <div style="background: rgba(2, 132, 199, 0.08); border-radius: 16px; padding: 18px; border: 2px solid rgba(2, 132, 199, 0.15); animation: fadeInUp 0.4s ease-out;">
            {pills_html}
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue to Severity Assessment →", type="primary", use_container_width=True):
                st.session_state.page = 'severity'
                st.rerun()
    else:
        st.info("👆 Please select at least one symptom to continue")

# ===== PAGE 2: SEVERITY RATING =====
elif st.session_state.page == 'severity':
    st.markdown("""
    <h2>📊 Step 2: Rate Symptom Severity</h2>
    <p style="color: #475569; font-size: 1.05rem;">How severe are your symptoms? This helps our AI assess risk levels accurately.</p>
    """, unsafe_allow_html=True)

    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← Back to Symptoms", use_container_width=True):
            st.session_state.page = 'input'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    for idx, symptom in enumerate(st.session_state.selected_symptoms):
        display_name = symptom.replace("_", " ").title()
        current = st.session_state.severity_levels.get(symptom, "moderate")

        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div style="padding: 18px; text-align: right;" class="animate-slideInLeft delay-{min(idx+1, 5)}">
                <span style="color: #0f172a; font-weight: 700; font-size: 1.1rem;">{display_name}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            severity = st.select_slider(
                "",
                options=["mild", "moderate", "severe"],
                value=current,
                key=f"sev_{symptom}"
            )
            st.session_state.severity_levels[symptom] = severity

            color = {"mild": "#10b981", "moderate": "#f59e0b", "severe": "#ef4444"}[severity]
            emoji = {"mild": "🟢", "moderate": "🟡", "severe": "🔴"}[severity]
            st.markdown(f"""
            <div style="margin-top: -8px;" class="animate-fadeIn delay-{min(idx+1, 5)}">
                <span style="color: {color}; font-weight: 700; font-size: 1rem;">
                    {emoji} {severity.upper()}
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h3 style='color: #0f172a;'>💊 Current Medications</h3>
    <p style="color: #475569; font-size: 1rem;">Enter any medicines you are currently taking (comma separated) to check for interactions:</p>
    """, unsafe_allow_html=True)

    cur_meds = st.text_input(
        "Medications",
        placeholder="e.g., Paracetamol, Ibuprofen, Aspirin...",
        label_visibility="collapsed"
    )
    cur_meds_list = [m.strip() for m in cur_meds.split(",") if m.strip()]

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔬 Run AI Diagnosis", type="primary", use_container_width=True):
            with st.spinner("🧠 Analyzing symptoms with multiple AI models..."):
                time.sleep(2)

                st.session_state.diagnosis_results = {
                    "symptoms": st.session_state.selected_symptoms,
                    "severity": st.session_state.severity_levels,
                    "medicines": cur_meds_list,
                    "patient_id": st.session_state.patient_id,
                    "age_group": st.session_state.age_group
                }
                st.session_state.page = 'results'
                st.rerun()

# ===== PAGE 3: RESULTS =====
elif st.session_state.page == 'results':
    results = st.session_state.diagnosis_results

    st.markdown("""
    <h2>📋 Step 3: Diagnosis Results</h2>
    """, unsafe_allow_html=True)

    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← New Diagnosis", use_container_width=True):
            st.session_state.page = 'input'
            st.session_state.selected_symptoms = []
            st.session_state.severity_levels = {}
            st.session_state.diagnosis_results = None
            st.rerun()

    if not MODULES_AVAILABLE:
        st.warning("⚠️ Running in **Demo Mode** — Backend modules not found. Connect your algorithms.py, ml_models.py, etc. for full functionality.")

        # DEMO DATA
        final = "Influenza (Flu)"
        base_risk = "MEDIUM"
        gs = 0.87
        ar = "Influenza"
        sev = "moderate"
        sc = 6
        top3 = [("Influenza", 87), ("COVID-19", 62), ("Malaria", 34)]
        ml_r = {"KNN": "Influenza", "SVM": "Influenza", "Neural Network": "Influenza"}
        acc = {"KNN": 85.7, "SVM": 92.3, "Neural Network": 88.9}
        risk = {"base_risk": "MEDIUM", "age_risk": "MEDIUM", "chronic_risk": "LOW", "treatment": ["Rest", "Hydration", "Oseltamivir", "Paracetamol"]}
        conflicts = []
        rec = ["Oseltamivir", "Paracetamol"]
        emergency = True

        # MAIN DIAGNOSIS CARD
        risk_color = {"LOW": "#10b981", "MEDIUM": "#f59e0b", "HIGH": "#f97316", "CRITICAL": "#ef4444"}.get(base_risk, "#f59e0b")
        risk_bg = {"LOW": "rgba(16, 185, 129, 0.15)", "MEDIUM": "rgba(245, 158, 11, 0.15)", "HIGH": "rgba(249, 115, 22, 0.15)", "CRITICAL": "rgba(239, 68, 68, 0.15)"}.get(base_risk, "rgba(245, 158, 11, 0.15)")

        st.markdown(f"""
        <div class="diagnosis-main">
            <div style="font-size: 3.5rem; margin-bottom: 15px; animation: float 3s ease-in-out infinite;">🦠</div>
            <h2 style="color: white; border: none; padding: 0; margin: 0; font-size: 1.8rem;">Primary Diagnosis</h2>
            <div style="font-size: 2.8rem; font-weight: 800; color: #ffffff; margin: 15px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                {final}
            </div>
            <div class="risk-badge" style="background: {risk_bg}; color: {risk_color}; border: 2px solid {risk_color};">
                ⚠️ {base_risk} RISK
            </div>
            <p style="color: #bae6fd; margin-top: 18px; font-size: 1rem; font-weight: 500;">
                Based on BFS + Minimax Algorithm | Confidence: {gs:.0%}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if emergency:
            st.markdown("""
            <div class="emergency-alert">
                <div style="font-size: 2.5rem; animation: bounce 1s infinite;">🚨</div>
                <h3 style="color: #dc2626; margin: 12px 0; font-size: 1.4rem;">EMERGENCY ALERT</h3>
                <p style="color: #991b1b; font-weight: 500;">Critical symptoms detected! Please seek immediate medical attention.</p>
            </div>
            """, unsafe_allow_html=True)

        # CHARTS SECTION
        if show_charts:
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='border-color: #6366f1;'>📊 Visual Analytics</h2>", unsafe_allow_html=True)

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                # Differential Diagnosis Bar Chart (Plotly)
                fig1 = go.Figure()
                diseases = [d[0] for d in top3]
                probs = [d[1] for d in top3]
                colors_bar = ['#0284c7', '#f59e0b', '#f97316']

                fig1.add_trace(go.Bar(
                    x=diseases,
                    y=probs,
                    marker_color=colors_bar,
                    text=[f'{p}%' for p in probs],
                    textposition='auto',
                    textfont=dict(size=14, color='white', family='Inter'),
                    hovertemplate='<b>%{x}</b><br>Probability: %{y}%<extra></extra>',
                ))
                fig1.update_layout(
                    title=dict(text='🔍 Differential Diagnosis', font=dict(size=18, color='#0f172a', family='Inter')),
                    xaxis_title='Disease',
                    yaxis_title='Probability (%)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#475569'),
                    xaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1'),
                    yaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1', range=[0, 100]),
                    margin=dict(t=50, b=40, l=40, r=20),
                    showlegend=False,
                )
                st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

            with chart_col2:
                # Model Accuracy Comparison
                fig2 = go.Figure()
                models = list(acc.keys())
                accuracies = list(acc.values())

                fig2.add_trace(go.Bar(
                    x=models,
                    y=accuracies,
                    marker_color=['#10b981', '#0284c7', '#6366f1'],
                    text=[f'{a}%' for a in accuracies],
                    textposition='auto',
                    textfont=dict(size=14, color='white', family='Inter'),
                    hovertemplate='<b>%{x}</b><br>Accuracy: %{y}%<extra></extra>',
                ))
                fig2.update_layout(
                    title=dict(text='🧠 ML Model Accuracy', font=dict(size=18, color='#0f172a', family='Inter')),
                    xaxis_title='Model',
                    yaxis_title='Accuracy (%)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#475569'),
                    xaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1'),
                    yaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1', range=[0, 100]),
                    margin=dict(t=50, b=40, l=40, r=20),
                    showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

            # Risk Gauge Chart
            gauge_col1, gauge_col2, gauge_col3 = st.columns([1,2,1])
            with gauge_col2:
                risk_value = {"LOW": 25, "MEDIUM": 50, "HIGH": 75, "CRITICAL": 95}.get(base_risk, 50)
                risk_gauge_color = {"LOW": "green", "MEDIUM": "orange", "HIGH": "orangered", "CRITICAL": "red"}.get(base_risk, "orange")

                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = risk_value,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "⚡ Risk Level", 'font': {'size': 22, 'color': '#0f172a', 'family': 'Inter'}},
                    number = {'font': {'size': 36, 'color': risk_color, 'family': 'Inter'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                        'bar': {'color': risk_color, 'thickness': 0.75},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "#e2e8f0",
                        'steps': [
                            {'range': [0, 33], 'color': 'rgba(16, 185, 129, 0.1)'},
                            {'range': [33, 66], 'color': 'rgba(245, 158, 11, 0.1)'},
                            {'range': [66, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=30, b=20, l=20, r=20),
                    height=300,
                )
                st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="result-card delay-1">
                <h3 style="color: #0284c7; margin-bottom: 18px; font-size: 1.2rem;">🤖 Algorithm Results</h3>
                <div class="info-box delay-1">
                    <span style="color: #475569; font-weight: 600;">BFS + Minimax:</span>
                    <span style="color: #0284c7; font-weight: 700; float: right;">Influenza</span>
                </div>
                <div class="info-box delay-2" style="border-color: #6366f1; background: linear-gradient(135deg, #eef2ff, #e0e7ff);">
                    <span style="color: #475569; font-weight: 600;">A* Best Match:</span>
                    <span style="color: #6366f1; font-weight: 700; float: right;">Influenza</span>
                </div>
                <div class="info-box delay-3" style="border-color: #7c3aed; background: linear-gradient(135deg, #f5f3ff, #ede9fe);">
                    <span style="color: #475569; font-weight: 600;">GBFS Confidence:</span>
                    <span style="color: #7c3aed; font-weight: 700; float: right;">87%</span>
                </div>
                <div class="info-box delay-4" style="border-color: #10b981; background: linear-gradient(135deg, #ecfdf5, #d1fae5);">
                    <span style="color: #475569; font-weight: 600;">Severity:</span>
                    <span style="color: #059669; font-weight: 700; float: right;">MODERATE (Score: 6/10)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Animated Differential Bars
            st.markdown("""
            <div class="result-card delay-2">
                <h3 style="color: #7c3aed; margin-bottom: 18px; font-size: 1.2rem;">🔍 Differential Diagnosis (Top 3)</h3>
            """, unsafe_allow_html=True)

            bar_colors = ["#0284c7", "#f59e0b", "#f97316"]
            for i, (d, p) in enumerate(top3):
                st.markdown(f"""
                <div style="margin: 12px 0;" class="animate-fadeInUp delay-{i+1}">
                    <div style="display: flex; align-items: center; margin-bottom: 6px;">
                        <span style="color: #0f172a; width: 130px; font-weight: 600; font-size: 0.95rem;">{d}</span>
                        <div class="animated-bar-bg">
                            <div class="animated-bar-fill" style="width: {p}%; background: linear-gradient(90deg, {bar_colors[i]}, {bar_colors[i]}dd);"></div>
                        </div>
                        <span style="color: {bar_colors[i]}; margin-left: 12px; font-weight: 700; font-size: 1rem;">{p}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="result-card delay-1">
                <h3 style="color: #10b981; margin-bottom: 18px; font-size: 1.2rem;">🧠 ML Model Predictions</h3>
            """, unsafe_allow_html=True)

            ml_colors = {"KNN": ("#10b981", "rgba(16, 185, 129, 0.1)", "#ecfdf5"), 
                         "SVM": ("#0284c7", "rgba(2, 132, 199, 0.1)", "#f0f9ff"), 
                         "Neural Network": ("#6366f1", "rgba(99, 102, 241, 0.1)", "#eef2ff")}

            for idx, (m, r) in enumerate(ml_r.items()):
                c, bg, bg2 = ml_colors.get(m, ("#475569", "rgba(71, 85, 105, 0.1)", "#f8fafc"))
                st.markdown(f"""
                <div style="margin: 12px 0; padding: 14px; background: linear-gradient(135deg, {bg2}, {bg}); border-radius: 14px; border-left: 4px solid {c}; animation: fadeInUp 0.5s ease-out {idx*0.15}s forwards; opacity: 0;" class="animate-fadeInUp delay-{idx+1}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #0f172a; font-weight: 700; font-size: 1.05rem;">{m}</span>
                        <span style="color: {c}; font-weight: 800; font-size: 1.1rem;">{r} ({acc[m]}%)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card delay-3">
                <h3 style="color: #ef4444; margin-bottom: 18px; font-size: 1.2rem;">⚡ Risk Assessment</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div style="text-align: center; padding: 18px; background: {risk_bg}; border-radius: 16px; border: 2px solid {risk_color}; animation: scaleIn 0.4s ease-out;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: {risk_color};">MEDIUM</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Base Risk</div>
                    </div>
                    <div style="text-align: center; padding: 18px; background: {risk_bg}; border-radius: 16px; border: 2px solid {risk_color}; animation: scaleIn 0.4s ease-out 0.1s forwards; opacity: 0;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: {risk_color};">MEDIUM</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Age Risk</div>
                    </div>
                    <div style="text-align: center; padding: 18px; background: rgba(16, 185, 129, 0.1); border-radius: 16px; border: 2px solid #10b981; animation: scaleIn 0.4s ease-out 0.2s forwards; opacity: 0;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: #059669;">LOW</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Chronic Risk</div>
                    </div>
                    <div style="text-align: center; padding: 18px; background: rgba(239, 68, 68, 0.1); border-radius: 16px; border: 2px solid #ef4444; animation: scaleIn 0.4s ease-out 0.3s forwards; opacity: 0;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: #dc2626;">HIGH</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Emergency</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="result-card delay-1">
                <h3 style="color: #0284c7; margin-bottom: 18px; font-size: 1.2rem;">💊 Recommended Treatment</h3>
                <ul style="color: #334155; line-height: 2.2; font-size: 1.05rem; font-weight: 500;">
                    <li>Rest and hydration</li>
                    <li>Antiviral medications (Oseltamivir)</li>
                    <li>Fever reducers (Paracetamol)</li>
                    <li>Monitor symptoms for 48 hours</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="result-card delay-2">
                <h3 style="color: #ef4444; margin-bottom: 18px; font-size: 1.2rem;">⚠️ Medicine Interactions</h3>
                <div style="padding: 18px; background: rgba(16, 185, 129, 0.08); border-radius: 14px; border: 2px solid #10b981; animation: fadeInUp 0.5s ease-out;">
                    <span style="color: #059669; font-weight: 700; font-size: 1.1rem;">✅ No conflicts detected</span>
                    <p style="color: #475569; font-size: 0.95rem; margin-top: 8px; line-height: 1.6;">Your current medications are safe to continue with the recommended treatment.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="result-card delay-1">
            <h3 style="color: #7c3aed; margin-bottom: 18px; font-size: 1.2rem;">🤖 AI Explanation</h3>
            <div style="background: linear-gradient(135deg, #f5f3ff, #faf5ff); border-radius: 16px; padding: 25px; border-left: 5px solid #7c3aed; animation: slideInLeft 0.6s ease-out;">
                <p style="color: #334155; line-height: 1.9; font-size: 1.05rem;">
                    <strong style="color: #7c3aed;">1. Symptom Analysis:</strong> The selected symptoms (fever, cough, fatigue, chills) strongly align with Influenza patterns in our knowledge base.<br><br>
                    <strong style="color: #7c3aed;">2. Algorithm Consensus:</strong> BFS traversal identified 3 candidate diseases. Minimax selected Influenza as the optimal choice with highest weighted score.<br><br>
                    <strong style="color: #7c3aed;">3. ML Validation:</strong> All three models (KNN, SVM, Neural Network) independently predicted Influenza, increasing confidence.<br><br>
                    <strong style="color: #7c3aed;">4. Risk Factors:</strong> Age group analysis shows medium risk. Severity scoring indicates moderate concern requiring monitoring.<br><br>
                    <strong style="color: #7c3aed;">5. Recommendation:</strong> Start treatment immediately. If symptoms worsen within 24-48 hours, seek emergency care.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        with st.expander("📄 View Complete Medical Report (JSON)"):
            report = {
                "Patient ID": st.session_state.patient_id,
                "Age Group": st.session_state.age_group,
                "Diagnosis": final,
                "Confidence": f"{gs:.0%}",
                "Severity": sev,
                "Base Risk": base_risk,
                "Age Risk": "MEDIUM",
                "Chronic Risk": "LOW",
                "Emergency": emergency,
                "Treatment": risk["treatment"],
                "Medicine Conflicts": conflicts,
                "Symptoms": st.session_state.selected_symptoms,
                "Severity Levels": st.session_state.severity_levels,
                "ML Predictions": {k: f"{v} ({acc[k]}%)" for k, v in ml_r.items()}
            }
            st.json(report)

        if voice_on:
            st.markdown("""
            <div style="text-align: center; margin: 25px 0; animation: fadeInUp 0.5s ease-out;">
                <div style="display: inline-block; background: linear-gradient(135deg, #e0f2fe, #bae6fd); border-radius: 50px; padding: 16px 35px; border: 2px solid #38bdf8;">
                    <span style="color: #0284c7; font-size: 1.15rem; font-weight: 600;">🔊 Voice diagnosis ready (gTTS)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # REAL MODULES MODE
        selected = results["symptoms"]
        sev_levels = results["severity"]
        age_group = results["age_group"]
        cur_meds_list = results["medicines"]
        patient_id = results["patient_id"]

        bfs_r = bfs_diagnose(selected, age_group)
        final = minimax_decision(bfs_r) if bfs_r else "Unknown"
        _, gs = gbfs_diagnose(selected, age_group)
        ar, _ = astar_path(selected, age_group)
        top3 = differential_diagnosis(selected, age_group)
        sev, sc = calculate_severity(selected, sev_levels)
        risk = get_risk_assessment(final, age_group)

        risk_color = {"LOW": "#10b981", "MEDIUM": "#f59e0b", "HIGH": "#f97316", "CRITICAL": "#ef4444"}.get(risk["base_risk"], "#f59e0b")
        risk_bg = {"LOW": "rgba(16, 185, 129, 0.15)", "MEDIUM": "rgba(245, 158, 11, 0.15)", "HIGH": "rgba(249, 115, 22, 0.15)", "CRITICAL": "rgba(239, 68, 68, 0.15)"}.get(risk["base_risk"], "rgba(245, 158, 11, 0.15)")

        st.markdown(f"""
        <div class="diagnosis-main">
            <div style="font-size: 3.5rem; margin-bottom: 15px; animation: float 3s ease-in-out infinite;">🏥</div>
            <h2 style="color: white; border: none; padding: 0; margin: 0; font-size: 1.8rem;">Primary Diagnosis</h2>
            <div style="font-size: 2.8rem; font-weight: 800; color: #ffffff; margin: 15px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                {final.title()}
            </div>
            <div class="risk-badge" style="background: {risk_bg}; color: {risk_color}; border: 2px solid {risk_color};">
                ⚠️ {risk["base_risk"]} RISK
            </div>
            <p style="color: #bae6fd; margin-top: 18px; font-size: 1rem; font-weight: 500;">
                Based on BFS + Minimax Algorithm | Confidence: {gs:.0%}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if check_emergency(final, selected):
            st.markdown("""
            <div class="emergency-alert">
                <div style="font-size: 2.5rem; animation: bounce 1s infinite;">🚨</div>
                <h3 style="color: #dc2626; margin: 12px 0; font-size: 1.4rem;">EMERGENCY ALERT</h3>
                <p style="color: #991b1b; font-weight: 500;">Critical symptoms detected! Please seek immediate medical attention.</p>
            </div>
            """, unsafe_allow_html=True)

        if show_charts:
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='border-color: #6366f1;'>📊 Visual Analytics</h2>", unsafe_allow_html=True)

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                fig1 = go.Figure()
                diseases = [d[0] for d in top3]
                probs = [d[1] for d in top3]
                colors_bar = ['#0284c7', '#f59e0b', '#f97316']

                fig1.add_trace(go.Bar(
                    x=diseases, y=probs, marker_color=colors_bar,
                    text=[f'{p}%' for p in probs], textposition='auto',
                    textfont=dict(size=14, color='white', family='Inter'),
                    hovertemplate='<b>%{x}</b><br>Probability: %{y}%<extra></extra>',
                ))
                fig1.update_layout(
                    title=dict(text='🔍 Differential Diagnosis', font=dict(size=18, color='#0f172a', family='Inter')),
                    xaxis_title='Disease', yaxis_title='Probability (%)',
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#475569'),
                    xaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1'),
                    yaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1', range=[0, 100]),
                    margin=dict(t=50, b=40, l=40, r=20), showlegend=False,
                )
                st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

            with chart_col2:
                sd = {s: 1 if s in selected else 0 for s in 
                      ["fever","cough","fatigue","thirst","chills",
                       "stomach_pain","shortness_of_breath","headache"]}
                ml_r = predict_all(sd)
                acc = get_model_accuracy()

                fig2 = go.Figure()
                models = list(acc.keys())
                accuracies = list(acc.values())

                fig2.add_trace(go.Bar(
                    x=models, y=accuracies,
                    marker_color=['#10b981', '#0284c7', '#6366f1'],
                    text=[f'{a}%' for a in accuracies], textposition='auto',
                    textfont=dict(size=14, color='white', family='Inter'),
                    hovertemplate='<b>%{x}</b><br>Accuracy: %{y}%<extra></extra>',
                ))
                fig2.update_layout(
                    title=dict(text='🧠 ML Model Accuracy', font=dict(size=18, color='#0f172a', family='Inter')),
                    xaxis_title='Model', yaxis_title='Accuracy (%)',
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#475569'),
                    xaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1'),
                    yaxis=dict(gridcolor='#e2e8f0', linecolor='#cbd5e1', range=[0, 100]),
                    margin=dict(t=50, b=40, l=40, r=20), showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

            gauge_col1, gauge_col2, gauge_col3 = st.columns([1,2,1])
            with gauge_col2:
                risk_value = {"LOW": 25, "MEDIUM": 50, "HIGH": 75, "CRITICAL": 95}.get(risk["base_risk"], 50)
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta", value=risk_value,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "⚡ Risk Level", 'font': {'size': 22, 'color': '#0f172a', 'family': 'Inter'}},
                    number={'font': {'size': 36, 'color': risk_color, 'family': 'Inter'}},
                    gauge={
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                        'bar': {'color': risk_color, 'thickness': 0.75},
                        'bgcolor': "white", 'borderwidth': 2, 'bordercolor': "#e2e8f0",
                        'steps': [
                            {'range': [0, 33], 'color': 'rgba(16, 185, 129, 0.1)'},
                            {'range': [33, 66], 'color': 'rgba(245, 158, 11, 0.1)'},
                            {'range': [66, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
                        ],
                        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=30, b=20, l=20, r=20), height=300,
                )
                st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="result-card delay-1">
                <h3 style="color: #0284c7; margin-bottom: 18px; font-size: 1.2rem;">🤖 Algorithm Results</h3>
                <div class="info-box delay-1">
                    <span style="color: #475569; font-weight: 600;">BFS + Minimax:</span>
                    <span style="color: #0284c7; font-weight: 700; float: right;">{final}</span>
                </div>
                <div class="info-box delay-2" style="border-color: #6366f1; background: linear-gradient(135deg, #eef2ff, #e0e7ff);">
                    <span style="color: #475569; font-weight: 600;">A* Best Match:</span>
                    <span style="color: #6366f1; font-weight: 700; float: right;">{ar}</span>
                </div>
                <div class="info-box delay-3" style="border-color: #7c3aed; background: linear-gradient(135deg, #f5f3ff, #ede9fe);">
                    <span style="color: #475569; font-weight: 600;">GBFS Confidence:</span>
                    <span style="color: #7c3aed; font-weight: 700; float: right;">{gs:.0%}</span>
                </div>
                <div class="info-box delay-4" style="border-color: #10b981; background: linear-gradient(135deg, #ecfdf5, #d1fae5);">
                    <span style="color: #475569; font-weight: 600;">Severity:</span>
                    <span style="color: #059669; font-weight: 700; float: right;">{sev.upper()} (Score: {sc})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="result-card delay-2">
                <h3 style="color: #7c3aed; margin-bottom: 18px; font-size: 1.2rem;">🔍 Differential Diagnosis (Top 3)</h3>
            """, unsafe_allow_html=True)

            bar_colors = ["#0284c7", "#f59e0b", "#f97316"]
            for i, (d, p) in enumerate(top3):
                st.markdown(f"""
                <div style="margin: 12px 0;" class="animate-fadeInUp delay-{i+1}">
                    <div style="display: flex; align-items: center; margin-bottom: 6px;">
                        <span style="color: #0f172a; width: 130px; font-weight: 600; font-size: 0.95rem;">{d}</span>
                        <div class="animated-bar-bg">
                            <div class="animated-bar-fill" style="width: {p}%; background: linear-gradient(90deg, {bar_colors[i]}, {bar_colors[i]}dd);"></div>
                        </div>
                        <span style="color: {bar_colors[i]}; margin-left: 12px; font-weight: 700; font-size: 1rem;">{p}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            sd = {s: 1 if s in selected else 0 for s in 
                  ["fever","cough","fatigue","thirst","chills",
                   "stomach_pain","shortness_of_breath","headache"]}
            ml_r = predict_all(sd)
            acc = get_model_accuracy()

            st.markdown("""
            <div class="result-card delay-1">
                <h3 style="color: #10b981; margin-bottom: 18px; font-size: 1.2rem;">🧠 ML Model Predictions</h3>
            """, unsafe_allow_html=True)

            ml_colors = {"KNN": ("#10b981", "rgba(16, 185, 129, 0.1)", "#ecfdf5"), 
                         "SVM": ("#0284c7", "rgba(2, 132, 199, 0.1)", "#f0f9ff"), 
                         "Neural Network": ("#6366f1", "rgba(99, 102, 241, 0.1)", "#eef2ff")}

            for idx, (m, r) in enumerate(ml_r.items()):
                c, bg, bg2 = ml_colors.get(m, ("#475569", "rgba(71, 85, 105, 0.1)", "#f8fafc"))
                st.markdown(f"""
                <div style="margin: 12px 0; padding: 14px; background: linear-gradient(135deg, {bg2}, {bg}); border-radius: 14px; border-left: 4px solid {c};" class="animate-fadeInUp delay-{idx+1}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #0f172a; font-weight: 700; font-size: 1.05rem;">{m}</span>
                        <span style="color: {c}; font-weight: 800; font-size: 1.1rem;">{r} ({acc[m]}%)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card delay-3">
                <h3 style="color: #ef4444; margin-bottom: 18px; font-size: 1.2rem;">⚡ Risk Assessment</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div style="text-align: center; padding: 18px; background: {risk_bg}; border-radius: 16px; border: 2px solid {risk_color}; animation: scaleIn 0.4s ease-out;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: {risk_color};">{risk["base_risk"]}</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Base Risk</div>
                    </div>
                    <div style="text-align: center; padding: 18px; background: {risk_bg}; border-radius: 16px; border: 2px solid {risk_color}; animation: scaleIn 0.4s ease-out 0.1s forwards; opacity: 0;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: {risk_color};">{risk["age_risk"]}</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Age Risk</div>
                    </div>
                    <div style="text-align: center; padding: 18px; background: rgba(16, 185, 129, 0.1); border-radius: 16px; border: 2px solid #10b981; animation: scaleIn 0.4s ease-out 0.2s forwards; opacity: 0;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: #059669;">{risk["chronic_risk"]}</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Chronic Risk</div>
                    </div>
                    <div style="text-align: center; padding: 18px; background: {'rgba(239, 68, 68, 0.1)' if check_emergency(final, selected) else 'rgba(16, 185, 129, 0.1)'}; border-radius: 16px; border: 2px solid {'#ef4444' if check_emergency(final, selected) else '#10b981'}; animation: scaleIn 0.4s ease-out 0.3s forwards; opacity: 0;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: {'#dc2626' if check_emergency(final, selected) else '#059669'};">{'HIGH' if check_emergency(final, selected) else 'LOW'}</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 6px; font-weight: 500;">Emergency</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        rec, conflicts = check_medicine_interaction(final, cur_meds_list)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="result-card delay-1">
    <h3 style="color: #0284c7; margin-bottom: 18px; font-size: 1.2rem;">💊 Recommended Treatment</h3>
    <ul style="color: #334155; line-height: 2.2; font-size: 1.05rem; font-weight: 500;">
        <li>Rest and hydration</li>
        <li>Antiviral medications (Oseltamivir)</li>
        <li>Fever reducers (Paracetamol)</li>
        <li>Monitor symptoms for 48 hours</li>
    </ul>
</div>
            """, unsafe_allow_html=True)

        with col2:
            if conflicts:
                st.markdown(f"""
                <div class="result-card delay-2">
                    <h3 style="color: #ef4444; margin-bottom: 18px; font-size: 1.2rem;">⚠️ Medicine Interactions</h3>
                    <div style="padding: 18px; background: rgba(239, 68, 68, 0.08); border-radius: 14px; border: 2px solid #ef4444; animation: fadeInUp 0.5s ease-out;">
                        <span style="color: #dc2626; font-weight: 700; font-size: 1.1rem;">❌ Conflicts: {conflicts}</span>
                        <p style="color: #475569; font-size: 0.95rem; margin-top: 8px; line-height: 1.6;">Please consult your doctor before taking these medications together.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card delay-2">
                    <h3 style="color: #ef4444; margin-bottom: 18px; font-size: 1.2rem;">⚠️ Medicine Interactions</h3>
                    <div style="padding: 18px; background: rgba(16, 185, 129, 0.08); border-radius: 14px; border: 2px solid #10b981; animation: fadeInUp 0.5s ease-out;">
                        <span style="color: #059669; font-weight: 700; font-size: 1.1rem;">✅ No conflicts detected</span>
                        <p style="color: #475569; font-size: 0.95rem; margin-top: 8px; line-height: 1.6;">Your current medications are safe to continue with the recommended treatment.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        exp = get_diagnosis_explanation(final, selected, risk["base_risk"], age_group)
        st.markdown(f"""
        <div class="result-card delay-1">
            <h3 style="color: #7c3aed; margin-bottom: 18px; font-size: 1.2rem;">🤖 AI Explanation</h3>
            <div style="background: linear-gradient(135deg, #f5f3ff, #faf5ff); border-radius: 16px; padding: 25px; border-left: 5px solid #7c3aed; animation: slideInLeft 0.6s ease-out;">
                <p style="color: #334155; line-height: 1.9; font-size: 1.05rem;">{exp}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        overlap = check_overlapping_diseases(bfs_r)
        if overlap and len(bfs_r) >= 2:
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
            overlap_exp = get_overlap_explanation(bfs_r[0][0], bfs_r[1][0], selected)
            st.markdown(f"""
            <div class="result-card delay-1">
                <h3 style="color: #f59e0b; margin-bottom: 18px; font-size: 1.2rem;">🔍 Overlap Analysis</h3>
                <div style="background: linear-gradient(135deg, #fffbeb, #fef3c7); border-radius: 16px; padding: 25px; border-left: 5px solid #f59e0b; animation: slideInLeft 0.6s ease-out;">
                    <p style="color: #334155; line-height: 1.9; font-size: 1.05rem;">{overlap_exp}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        save_patient_history(patient_id, selected, final, age_group)
        if show_hist:
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="result-card delay-1">
                <h3 style="color: #0284c7; margin-bottom: 18px; font-size: 1.2rem;">📋 Patient History</h3>
            </div>
            """, unsafe_allow_html=True)
            get_patient_history(patient_id)

        if show_cm:
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="result-card delay-1">
                <h3 style="color: #0284c7; margin-bottom: 18px; font-size: 1.2rem;">📊 Confusion Matrix (KNN)</h3>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(get_confusion_matrix("knn"), use_container_width=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        with st.expander("📄 View Complete Medical Report (JSON)"):
            report = {
                "Patient ID": patient_id,
                "Age Group": age_group,
                "Diagnosis": final,
                "Severity": sev,
                "Base Risk": risk["base_risk"],
                "Age Risk": risk["age_risk"],
                "Chronic Risk": risk["chronic_risk"],
                "Treatment": risk.get("treatment", []),
                "Recommended Meds": rec,
                "Medicine Conflicts": conflicts,
                "Symptoms": selected,
                "Severity Levels": sev_levels,
                "ML Predictions": ml_r
            }
            st.json(report)

        if voice_on:
            audio = speak(f"Diagnosis complete. You likely have {final}. Risk level is {risk['base_risk']}.")
            st.audio(audio, format="audio/mp3")
