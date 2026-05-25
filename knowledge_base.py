diseases = {
    "flu": {
        "symptoms": {
            "fever": 3,           # weight — kitna common hai is disease mein
            "cough": 3,
            "fatigue": 2,
            "body ache": 2,
            "runny nose": 1
        },
        "risk_level": "LOW",
        "treatment": "Rest, fluids, paracetamol",
        "age_risk": {"child": "HIGH", "adult": "LOW", "elderly": "HIGH"}
    },
    "malaria": {
        "symptoms": {
            "fever": 3,
            "chills": 3,
            "sweating": 2,
            "headache": 2,
            "nausea": 1
        },
        "risk_level": "HIGH",
        "treatment": "Antimalarial drugs, consult doctor immediately",
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"}
    },
    "covid": {
        "symptoms": {
            "fever": 3,
            "cough": 3,
            "loss of smell": 3,
            "fatigue": 2,
            "breathlessness": 3
        },
        "risk_level": "HIGH",
        "treatment": "Isolation, rest, consult doctor",
        "age_risk": {"child": "LOW", "adult": "MEDIUM", "elderly": "CRITICAL"}
    },
    "diabetes": {
        "symptoms": {
            "thirst": 3,
            "frequent urination": 3,
            "blurred vision": 2,
            "fatigue": 2,
            "slow healing": 3
        },
        "risk_level": "HIGH",
        "treatment": "Insulin therapy, controlled diet, regular checkups",
        "age_risk": {"child": "HIGH", "adult": "HIGH", "elderly": "CRITICAL"}
    },
    "typhoid": {
        "symptoms": {
            "fever": 3,
            "stomach pain": 3,
            "weakness": 2,
            "headache": 2,
            "loss of appetite": 2
        },
        "risk_level": "HIGH",
        "treatment": "Antibiotics, bed rest, clean water",
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "HIGH"}
    },
    "pneumonia": {
        "symptoms": {
            "cough": 3,
            "fever": 3,
            "chest pain": 3,
            "shortness of breath": 3,
            "sweating": 1
        },
        "risk_level": "CRITICAL",
        "treatment": "Antibiotics, hospital if severe",
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"}
    },
    "dengue": {
        "symptoms": {
            "fever": 3,
            "severe headache": 3,
            "joint pain": 3,
            "rash": 2,
            "nausea": 1
        },
        "risk_level": "HIGH",
        "treatment": "Fluids, rest, avoid aspirin",
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"}
    },
    "tuberculosis": {
        "symptoms": {
            "cough": 3,
            "weight loss": 3,
            "night sweats": 3,
            "fatigue": 2,
            "chest pain": 2
        },
        "risk_level": "CRITICAL",
        "treatment": "6 month antibiotic course, DOTS therapy",
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"}
    },
    "hepatitis": {
        "symptoms": {
            "jaundice": 3,
            "fatigue": 2,
            "nausea": 2,
            "stomach pain": 2,
            "dark urine": 3
        },
        "risk_level": "HIGH",
        "treatment": "Antiviral drugs, avoid alcohol",
        "age_risk": {"child": "HIGH", "adult": "HIGH", "elderly": "CRITICAL"}
    },
    "asthma": {
        "symptoms": {
            "shortness of breath": 3,
            "wheezing": 3,
            "chest tightness": 3,
            "cough": 2
        },
        "risk_level": "MEDIUM",
        "treatment": "Inhaler, avoid triggers, bronchodilators",
        "age_risk": {"child": "HIGH", "adult": "MEDIUM", "elderly": "HIGH"}
    },
    "hypertension": {
        "symptoms": {
            "headache": 2,
            "dizziness": 2,
            "blurred vision": 2,
            "chest pain": 3,
            "nausea": 1
        },
        "risk_level": "HIGH",
        "treatment": "Low salt diet, exercise, BP medication",
        "age_risk": {"child": "LOW", "adult": "HIGH", "elderly": "CRITICAL"}
    },
    "anemia": {
        "symptoms": {
            "fatigue": 3,
            "pale skin": 3,
            "weakness": 2,
            "dizziness": 2,
            "shortness of breath": 2
        },
        "risk_level": "MEDIUM",
        "treatment": "Iron supplements, iron rich diet",
        "age_risk": {"child": "HIGH", "adult": "MEDIUM", "elderly": "HIGH"}
    },
    "gastroenteritis": {
        "symptoms": {
            "diarrhea": 3,
            "vomiting": 3,
            "stomach pain": 2,
            "nausea": 2,
            "fever": 1
        },
        "risk_level": "MEDIUM",
        "treatment": "ORS fluids, rest, bland diet",
        "age_risk": {"child": "HIGH", "adult": "LOW", "elderly": "HIGH"}
    },
    "chickenpox": {
        "symptoms": {
            "rash": 3,
            "fever": 2,
            "itching": 3,
            "fatigue": 1,
            "loss of appetite": 1
        },
        "risk_level": "LOW",
        "treatment": "Calamine lotion, antihistamines, rest",
        "age_risk": {"child": "LOW", "adult": "MEDIUM", "elderly": "HIGH"}
    },
    "measles": {
        "symptoms": {
            "fever": 3,
            "rash": 3,
            "cough": 2,
            "runny nose": 2,
            "red eyes": 3
        },
        "risk_level": "HIGH",
        "treatment": "Rest, fluids, vitamin A",
        "age_risk": {"child": "HIGH", "adult": "MEDIUM", "elderly": "HIGH"}
    },
    "migraine": {
        "symptoms": {
            "severe headache": 3,
            "nausea": 2,
            "sensitivity to light": 3,
            "vomiting": 2,
            "dizziness": 2
        },
        "risk_level": "LOW",
        "treatment": "Pain relievers, rest in dark room",
        "age_risk": {"child": "LOW", "adult": "LOW", "elderly": "MEDIUM"}
    },
    "urinary tract infection": {
        "symptoms": {
            "frequent urination": 3,
            "burning urination": 3,
            "lower stomach pain": 3,
            "fever": 1,
            "cloudy urine": 2
        },
        "risk_level": "MEDIUM",
        "treatment": "Antibiotics, drink plenty of water",
        "age_risk": {"child": "MEDIUM", "adult": "LOW", "elderly": "HIGH"}
    },
    "food poisoning": {
        "symptoms": {
            "vomiting": 3,
            "diarrhea": 3,
            "stomach pain": 2,
            "nausea": 2,
            "fever": 1
        },
        "risk_level": "MEDIUM",
        "treatment": "ORS fluids, rest, avoid solid food",
        "age_risk": {"child": "HIGH", "adult": "LOW", "elderly": "HIGH"}
    },
    "allergy": {
        "symptoms": {
            "sneezing": 3,
            "runny nose": 2,
            "itching": 3,
            "rash": 2,
            "watery eyes": 3
        },
        "risk_level": "LOW",
        "treatment": "Antihistamines, avoid allergens",
        "age_risk": {"child": "MEDIUM", "adult": "LOW", "elderly": "LOW"}
    },
    "depression": {
        "symptoms": {
            "sadness": 3,
            "fatigue": 2,
            "loss of interest": 3,
            "sleep problems": 3,
            "poor concentration": 2
        },
        "risk_level": "HIGH",
        "treatment": "Therapy, antidepressants, social support",
        "age_risk": {"child": "HIGH", "adult": "HIGH", "elderly": "HIGH"}
    },
}

print(f"Upgraded Knowledge Base loaded!")
print(f"Total diseases: {len(diseases)}")
print(f"Features: Symptom weights + Risk levels + Age risk!")
