import json
from openai import OpenAI
from setting.config import *




def gen_openai_client():
    try:
        openai_key = config.OPENAI_KEY
        if not openai_key:
            raise KeyError("OPEN AI key is not loaded")
        client = OpenAI(api_key=openai_key)
        return client
    except KeyError as e:
        raise e
    except Exception as e:
        print(f"error in connecting to open ai api. error: {str(e)}")
        raise e


def get_openai_response(prompt: str) -> dict:
    try:
        client = gen_openai_client()
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
            except json.JSONDecodeError as e:
                print({"error": "Response is not valid JSON", "response": response})
                raise e
        except Exception as e:
            print(f"error in generating question with openai api: e: {str(e)}")
            raise e
    except KeyError as e:
        raise e
    except Exception as e:
        print(f"error in connecting to open ai api. error: {str(e)}")
        raise e
