def generate_question_prompt(topic:str, difficulty:str | None = None) -> str:
    prompt = f"Give me a technical question, answer and explanation on  the topic: {topic}."
    prompt += """
    Return them in a dictionary format with the keys: 'question', 'answer', 'explanation'.
    The answer should be short and to the point, while the explanation goes into
    more technical details and code examples. Don't add anything else to the response
    - just the dict. Limit the question length to 100 chars. use double quotes for the dict keys.
    """
    if difficulty is not None:
        prompt += f"The question level should be: {difficulty}"  
    return prompt
  