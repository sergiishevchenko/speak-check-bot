from typing import Tuple
from google.cloud import dialogflow


def get_intent(project_id: str, session_id: str, msg: str, language_code: str) -> Tuple[str, bool]:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=msg, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

    return response.query_result