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
    Patient has symptoms: {', '.join(symptoms)}
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

def get_severity_advice(disease, severity, symptoms):
    prompt = f"""
    Patient has {disease} with {severity} severity.
    Symptoms: {', '.join(symptoms)}
    In 3 lines give:
    1. What {severity} severity means for {disease}
    2. Should they go to hospital or stay home?
    3. One most important thing to do right now
    """
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content

def get_medicine_advice(disease, conflicts):
    if conflicts:
        conflict_text = ', '.join(conflicts)
        prompt = f"""
        Patient with {disease} has medicine conflicts: {conflict_text}
        In 2 lines:
        1. How dangerous is this combination
        2. What should patient do immediately
        """
    else:
        prompt = f"""
        Patient diagnosed with {disease}.
        In 2 lines give general medicine safety advice for this disease.
        """
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content

def get_chronic_advice(disease, visit_count):
    prompt = f"""
    Patient has visited {visit_count} times with same disease: {disease}
    In 2 lines:
    1. What does repeated {disease} mean
    2. What long term steps should they take
    """
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content

print("Advanced Groq Diagnosis loaded!")
print("Features: Explanation + Overlap + Severity + Medicine + Chronic Advice!")
