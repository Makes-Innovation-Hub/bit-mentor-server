from server.utils.open_ai import get_openai_response, get_question_and_answer_and_explanation


def test_get_openai_response_contains_keys():
    prompt = "Python"
    response, error = get_question_and_answer_and_explanation(prompt)

    if error:
        # Handle case when there is an error
        assert isinstance(response, dict)
        assert "error" in response
        print(f"Error in response: {response['error']}")
    else:
        # Handle case when there is no error
        assert isinstance(response, dict)
        assert "question" in response
        assert "answer" in response
        assert "explanation" in response


def manual_testing_openai():
    prompt_text = input("Enter your prompt: ")
    result, error = get_openai_response(prompt_text)
    print("Regular Response from OpenAI:")
    print(result)

    difficulty_levels = ["easy", "medium", "hard", "impossible"]
    for level in difficulty_levels:
        result, error = get_question_and_answer_and_explanation(prompt_text, level)
        print(f"Custom Function Response from OpenAI for {level} difficulty:")
        print(result)


if __name__ == "__main__":
    manual_testing_openai()
    test_get_openai_response_contains_keys()
