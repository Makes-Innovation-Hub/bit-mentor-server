import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_response(prompt):
    API_KEY = os.getenv("OPENAI_KEY")
    if not API_KEY:
        return {"error": "API key not provided. Please set the OPENAI_KEY environment variable."}, True
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
        response_json = response.json()
        if 'choices' in response_json and 'message' in response_json['choices'][0]:
            return response_json['choices'][0]['message']['content'], False  # False indicates no error
        else:
            return {"error": "No valid response in 'choices'."}, True  # True indicates an error occurred
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, True


def generate_question(topic):
    prompt = f"Create a trivia question about {topic}. The question should be no longer than 100 characters."
    response, error = get_openai_response(prompt)
    if error:
        return {"error": response}

    prompt = f"Provide a detailed explanation for the answer to the question: {response}"
    explanation, error = get_openai_response(prompt)
    if error:
        return {"error": explanation}

    return {"question": response, "explanation": explanation}
