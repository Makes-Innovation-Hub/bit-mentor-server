import requests
import os

from dotenv import load_dotenv

load_dotenv()


def create_header(API_KEY):
    return {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }


def format_data(prompt):
    return {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }


def create_question_and_answer_and_explanation(subject):
    return f"give me a question,answer and explanation on {subject}.return them in a dictionary format. limit the question length to 100 chars"


def get_question_and_answer_and_explanation(prompt):
    prompt = create_question_and_answer_and_explanation(prompt)
    return get_openai_response(prompt)


def get_openai_response(prompt):
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    if not OPENAI_KEY:
        return "API key not provided. Please set the OPENAI_KEY environment variable.", True

    headers = create_header(OPENAI_KEY)

    data = format_data(prompt)

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
        response_json = response.json()
        if 'choices' in response_json and 'message' in response_json['choices'][0]:
            return response_json['choices'][0]['message']['content'], False  # False indicates no error
        else:
            return "No valid response in 'choices'.", True  # True indicates an error occurred
    except Exception as e:
        return f"An error occurred: {str(e)}", True


