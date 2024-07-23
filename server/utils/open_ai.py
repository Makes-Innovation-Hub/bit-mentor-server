import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


def create_question_and_answer_and_explanation(subject):
    return (f"Give me a question, answer, and explanation on {subject}. Return them in a dictionary format with the "
            f"keys 'question' 'answer' 'explanation'. Limit the question length to 100 chars.")


def get_question_and_answer_and_explanation(prompt):
    prompt = create_question_and_answer_and_explanation(prompt)
    return get_openai_response(prompt)


def get_openai_response(prompt):
    if not client.api_key:
        return "API key not provided. Please set the OPENAI_KEY environment variable.", True
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
        )
        response = chat_completion.choices[0].message.content
        try:
            response_json = json.loads(response)
            return response_json, False  # False indicates no error
        except json.JSONDecodeError:
            return response, False
    except Exception as e:
        return f"An error occurred: {str(e)}", True


if __name__ == "__main__":
    prompt_text = input("Enter your prompt: ")
    result, error = get_openai_response(prompt_text)
    print("Regular Response from OpenAI:")
    print(result)
    result, error = get_question_and_answer_and_explanation(prompt_text)
    print("Custom Function Response from OpenAI:")
    print(result)
    print(result['question'])
