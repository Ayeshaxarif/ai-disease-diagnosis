import os
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_diagnosis_explanation(disease, symptoms):
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{
            'role': 'user',
            'content': f'Patient has symptoms: {symptoms}. Diagnosed with: {disease}. Give a brief 3 line explanation and treatment advice.'
        }]
    )
    return response.choices[0].message.content

print("Groq diagnosis ready!")
