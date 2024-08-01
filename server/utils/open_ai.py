import json
import os
from openai import OpenAI
from dotenv import load_dotenv

from server.utils.logger import app_logger

load_dotenv()


def gen_openai_client():
    try:
        openai_key = os.getenv("OPENAI_KEY")
        if not openai_key:
            app_logger.error("OPEN AI key is not loaded")
            raise KeyError("OPEN AI key is not loaded")
        client = OpenAI(api_key=openai_key)
        app_logger.info("OpenAI client initialized successfully")
        return client
    except KeyError as e:
        app_logger.error(f"KeyError: {str(e)}")
        raise e
    except Exception as e:
        print(f"error in connecting to open ai api. error: {str(e)}")
        app_logger.error(f"Error initializing OpenAI client: {str(e)}")
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
            app_logger.info(f"OpenAI response received: {response}")
            try:
                response_json = json.loads(response)
                return response_json
            except json.JSONDecodeError as e:
                app_logger({"error": "Response is not valid JSON", "response": response})
                raise e
        except Exception as e:
            app_logger.error(f"error in generating question with openai api: e: {str(e)}")
            raise e
    except KeyError as e:
        app_logger.error(f"KeyError: {str(e)}")
        raise e
    except Exception as e:
        app_logger.error(f"error in connecting to open ai api. error: {str(e)}")
        raise e
