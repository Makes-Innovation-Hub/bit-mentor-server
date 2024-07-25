from data_types.gen_question_body import QuestionRequest


def generate_question_prompt(topic: str, difficulty: str | None = None) -> str:
    prompt = f"Give me a technical question, answer and explanation on  the topic: {topic}."
    prompt += """
    Return them in a dictionary format with the keys: 'question', 'answer', 'explanation'.
    The answer should be short and to the point, while the explanation goes into
    more technical details and code examples. Don't add anything else to the response
    - just the dict. Limit the question length to 100 chars. use double quotes for the dict keys.
    Include the subject inside the question.
    """
    if difficulty is not None:
        prompt += f"The question level should be: {difficulty}"
    return prompt


def create_question_with_multiple_options(request: QuestionRequest):
    prompt = (
        f"Give me a question, {request.answers_count} answer choices, and explanations on {request.subject}. "
        f"Return them in a dictionary format with the keys 'question_text', 'options', 'details',"
        f" and 'correct_answer'. "
        f"Limit the question length to 100 characters. Use double quotes for the dict keys. "
        f"Make sure the answers do not include any fluff. "
        f"Format the response like this: "
        f'{{"question_text": "Sample question?", '
        f'"options": ["Option 1", "Option 2", "Option 3", "Option 4"], '
        f'"details": ["Explanation for Option 1", "Explanation for Option 2", "Explanation for Option 3"'
        f', "Explanation for Option 4"], '
        f'"correct_answer": 1}}'
    )

    if request.difficulty:
        prompt += f" Ensure the question level is {request.difficulty}."

    return prompt
