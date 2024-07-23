####################################################################
#create promps for AI
def create_difficulty_question_and_answer_and_explanation(subject, difficulty):
    str = create_question_and_answer_and_explanation(subject)
    if difficulty is not None:
      str += f"the question level {difficulty}"
    return str


def create_question_and_answer_and_explanation(subject):
    return (f"Give me a question, answer, and explanation on {subject}. Return them in a dictionary format with the "
            f"keys 'question' 'answer' 'explanation'. Limit the question length to 100 chars. use double quotes for the dict keys")

