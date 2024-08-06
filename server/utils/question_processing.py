from data_types.question_models import QuestionResponse


def process_question_request(result,with_answers):

    if with_answers:
        question_text = result["question_text"]
        options = result["options"]
        details = result["details"]
        correct_answer = result["correct_answer"]
        answer = ""
    else:
        question_text = result["question_text"]
        details = [result["details"]]
        options = details
        correct_answer = 0
        answer = result["answer"]

    return QuestionResponse(
        question_text=question_text,
        options=options,
        details=details,
        correct_answer=correct_answer,
        answer = answer
    )
