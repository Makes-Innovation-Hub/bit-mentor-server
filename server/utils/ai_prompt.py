####################################################################
# create promps for AI
from schemas.question import QuestionRequest


def create_difficulty_question_and_answer_and_explanation(subject, difficulty):
    str = create_question_and_answer_and_explanation(subject)
    if difficulty is not None:
        str += f"the question level {difficulty}"
    return str


def create_question_and_answer_and_explanation(subject):
    return (f"Give me a question, answer, and explanation on {subject}. Return them in a dictionary format with the "
            f"keys 'question' 'answer' 'explanation'. Limit the question length to 100 chars. use double quotes for the dict keys")


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
