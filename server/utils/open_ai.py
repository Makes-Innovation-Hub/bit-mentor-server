import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


def get_openai_response(prompt):
    if not client.api_key:
        return {"error": "API key not provided. Please set the OPENAI_KEY environment variable."}, True
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": "You are a teacher teaching subject to student by asking good helpful questions."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
        )
        response = chat_completion.choices[0].message.content
        try:
            response_json = json.loads(response)
            return response_json
        except json.JSONDecodeError:
            return {"error": "Response is not valid JSON", "response": response}, True
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, True
