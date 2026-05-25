diseases = {
    "flu": {
        "symptoms": {
            "fever": 3,
            "cough": 3,
            "fatigue": 2,
            "body ache": 2,
            "runny nose": 1
        },
        "risk_level": "LOW",
        "treatment": "Rest, fluids, paracetamol",
        "age_risk": {"child": "HIGH", "adult": "LOW", "elderly": "HIGH"},
        "medicines": ["paracetamol", "ibuprofen", "antihistamine"],
        "emergency_symptoms": ["difficulty breathing", "chest pain", "confusion"],
        "chronic_risk": "LOW"
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
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"},
        "medicines": ["chloroquine", "artemisinin", "paracetamol"],
        "emergency_symptoms": ["seizures", "unconsciousness", "severe anemia"],
        "chronic_risk": "MEDIUM"
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
        "age_risk": {"child": "LOW", "adult": "MEDIUM", "elderly": "CRITICAL"},
        "medicines": ["paracetamol", "vitamin c", "zinc"],
        "emergency_symptoms": ["breathlessness", "chest pain", "confusion", "blue lips"],
        "chronic_risk": "HIGH"
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
        "age_risk": {"child": "HIGH", "adult": "HIGH", "elderly": "CRITICAL"},
        "medicines": ["insulin", "metformin", "glipizide"],
        "emergency_symptoms": ["unconsciousness", "extreme thirst", "fruity breath"],
        "chronic_risk": "CRITICAL"
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
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "HIGH"},
        "medicines": ["ciprofloxacin", "azithromycin", "paracetamol"],
        "emergency_symptoms": ["intestinal bleeding", "perforation", "shock"],
        "chronic_risk": "LOW"
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
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"},
        "medicines": ["amoxicillin", "azithromycin", "paracetamol"],
        "emergency_symptoms": ["blue lips", "rapid breathing", "chest pain"],
        "chronic_risk": "MEDIUM"
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
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"},
        "medicines": ["paracetamol", "oral rehydration salts"],
        "emergency_symptoms": ["bleeding gums", "blood in urine", "severe abdominal pain"],
        "chronic_risk": "LOW"
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
        "age_risk": {"child": "CRITICAL", "adult": "HIGH", "elderly": "CRITICAL"},
        "medicines": ["isoniazid", "rifampicin", "pyrazinamide"],
        "emergency_symptoms": ["coughing blood", "severe weight loss", "breathing failure"],
        "chronic_risk": "CRITICAL"
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
        "age_risk": {"child": "HIGH", "adult": "HIGH", "elderly": "CRITICAL"},
        "medicines": ["interferon", "ribavirin", "vitamin b complex"],
        "emergency_symptoms": ["liver failure", "severe jaundice", "confusion"],
        "chronic_risk": "CRITICAL"
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
        "age_risk": {"child": "HIGH", "adult": "MEDIUM", "elderly": "HIGH"},
        "medicines": ["salbutamol", "budesonide", "montelukast"],
        "emergency_symptoms": ["severe breathlessness", "blue lips", "cannot speak"],
        "chronic_risk": "HIGH"
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
        "age_risk": {"child": "LOW", "adult": "HIGH", "elderly": "CRITICAL"},
        "medicines": ["amlodipine", "lisinopril", "atenolol"],
        "emergency_symptoms": ["stroke symptoms", "heart attack", "vision loss"],
        "chronic_risk": "CRITICAL"
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
        "age_risk": {"child": "HIGH", "adult": "MEDIUM", "elderly": "HIGH"},
        "medicines": ["ferrous sulfate", "vitamin b12", "folic acid"],
        "emergency_symptoms": ["heart palpitations", "fainting", "extreme weakness"],
        "chronic_risk": "MEDIUM"
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
        "age_risk": {"child": "HIGH", "adult": "LOW", "elderly": "HIGH"},
        "medicines": ["oral rehydration salts", "ondansetron", "probiotics"],
        "emergency_symptoms": ["severe dehydration", "blood in stool", "high fever"],
        "chronic_risk": "LOW"
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
        "age_risk": {"child": "LOW", "adult": "MEDIUM", "elderly": "HIGH"},
        "medicines": ["calamine lotion", "antihistamine", "paracetamol"],
        "emergency_symptoms": ["bacterial infection of rash", "pneumonia", "encephalitis"],
        "chronic_risk": "LOW"
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
        "age_risk": {"child": "HIGH", "adult": "MEDIUM", "elderly": "HIGH"},
        "medicines": ["vitamin a", "paracetamol", "antibiotics if secondary infection"],
        "emergency_symptoms": ["encephalitis", "pneumonia", "severe rash spreading"],
        "chronic_risk": "LOW"
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
        "age_risk": {"child": "LOW", "adult": "LOW", "elderly": "MEDIUM"},
        "medicines": ["sumatriptan", "ibuprofen", "paracetamol"],
        "emergency_symptoms": ["worst headache of life", "vision loss", "paralysis"],
        "chronic_risk": "MEDIUM"
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
        "age_risk": {"child": "MEDIUM", "adult": "LOW", "elderly": "HIGH"},
        "medicines": ["trimethoprim", "nitrofurantoin", "ciprofloxacin"],
        "emergency_symptoms": ["kidney pain", "high fever", "blood in urine"],
        "chronic_risk": "MEDIUM"
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
        "age_risk": {"child": "HIGH", "adult": "LOW", "elderly": "HIGH"},
        "medicines": ["oral rehydration salts", "ondansetron", "activated charcoal"],
        "emergency_symptoms": ["severe dehydration", "bloody diarrhea", "high fever"],
        "chronic_risk": "LOW"
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
        "age_risk": {"child": "MEDIUM", "adult": "LOW", "elderly": "LOW"},
        "medicines": ["cetirizine", "loratadine", "fexofenadine"],
        "emergency_symptoms": ["anaphylaxis", "throat swelling", "difficulty breathing"],
        "chronic_risk": "MEDIUM"
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
        "age_risk": {"child": "HIGH", "adult": "HIGH", "elderly": "HIGH"},
        "medicines": ["sertraline", "fluoxetine", "counseling"],
        "emergency_symptoms": ["suicidal thoughts", "self harm", "complete withdrawal"],
        "chronic_risk": "HIGH"
    },
}

print(f"Advanced Knowledge Base loaded!")
print(f"Total diseases: {len(diseases)}")
print(f"Features: Weights + Risk + Age Risk + Medicines + Emergency Symptoms + Chronic Risk!")
