from server.utils.open_ai import *
from unittest.mock import patch, Mock


@patch('requests.post')
def test_get_openai_response_success(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {
        'choices': [{
            'message': {
                'content': 'Sample question, answer and explanation'
            }
        }]
    }
    mock_post.return_value = mock_response

    response, error = get_openai_response("Sample prompt")
    assert not error
    assert response == 'Sample question, answer and explanation'


@patch('requests.post')
def test_get_openai_response_failure(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {}
    mock_post.return_value = mock_response

    response, error = get_openai_response("Sample prompt")
    assert error
    assert response == "No valid response in 'choices'."


@patch('requests.post', side_effect=Exception('Test exception'))
def test_get_openai_response_exception(mock_post):
    response, error = get_openai_response("Sample prompt")
    assert error
    assert "An error occurred: Test exception" in response


@patch('requests.post')
def test_get_openai_response_no_api_key(mock_post):
    with patch.dict('os.environ', {'OPENAI_KEY': ''}):
        response, error = get_openai_response("Sample prompt")
        assert error
        assert response == "API key not provided. Please set the OPENAI_KEY environment variable."


@patch('requests.post')
def test_format_data(mock_post):
    prompt = "Sample prompt"
    formatted_data = format_data(prompt)
    expected_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    assert formatted_data == expected_data


@patch('requests.post')
def test_create_header(mock_post):
    api_key = "test_key"
    headers = create_header(api_key)
    expected_headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    assert headers == expected_headers


@patch('requests.post')
def test_create_question_and_answer_and_explanation(mock_post):
    subject = "Python programming"
    result = create_question_and_answer_and_explanation(subject)
    expected_result = "give me a question,answer and explanation on Python programming.return them in a dictionary format. limit the question length to 100 chars"
    assert result == expected_result
