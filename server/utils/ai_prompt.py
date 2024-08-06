from data_types.question_models import QuestionRequest


def generate_question_prompt(question: QuestionRequest) -> str:
    prompt = f"Give me a {question.difficulty} technical question, answer and explanation on  the topic: " \
             f"{question.subject}."
    prompt += """
    Return them in a dictionary format with the keys: 'question_text', 'answer', 'details'.
    The answer should be short and to the point, while the explanation goes into
    more technical details and code examples. Don't add anything else to the response
    - just the dict. Limit the question length to 100 chars. use double quotes for the dict keys.
    Include the subject inside the question.
    """
    return prompt


def generate_question_with_multiple_options(question: QuestionRequest) -> str:
    print("generate_question_with_multiple_options")
    prompt = (
        f"Generate a {question.difficulty} question with {question.answers_count} answer choices and explanations on "
        f"{question.subject} suitable for a computer science graduate. "
        f"Return the result in a dictionary format with the following keys: "
        f"'question_text', 'options', 'details', and 'correct_answer'. "
        f"The question should be no longer than 100 characters. "
        f"Ensure that the answer options are concise and use double quotes for all keys in the dictionary. "
        f"Format your response as follows: "
        f'{{"question_text": "question?", '
        f'"options": ["Option 0", "Option 1", "Option 2", "Option 3"], '
        f'"details": ["Explanation for Option 0", "Explanation for Option 1", "Explanation for Option 2", '
        f'"Explanation for Option 3"], '
        f'"correct_answer": the index of the correct option}}'
    )

    return prompt
