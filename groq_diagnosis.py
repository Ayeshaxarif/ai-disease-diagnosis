import os
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_diagnosis_explanation(disease, symptoms, risk_level, age_group):
    prompt = f"""
    Patient Information:
    - Age Group: {age_group}
    - Symptoms: {', '.join(symptoms)}
    - Diagnosed Disease: {disease}
    - Risk Level: {risk_level}

    Please provide:
    1. Brief explanation of the disease (2 lines)
    2. Why these symptoms match this disease
    3. Immediate steps patient should take
    4. Warning signs to watch out for
    5. Is doctor visit required? Yes or No and why

    Keep response clear and simple.
    """
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content

def get_overlap_explanation(disease1, disease2, symptoms):
    prompt = f"""
    A patient has symptoms: {', '.join(symptoms)}
    Both {disease1} and {disease2} are possible diagnoses.
    
    In 3 lines explain:
    1. Why both are possible
    2. Key difference between {disease1} and {disease2}
    3. What additional symptom would confirm which one it is
    """
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content

print("Upgraded Groq Diagnosis loaded!")
print("Features: Detailed explanation + Overlap analysis!")
