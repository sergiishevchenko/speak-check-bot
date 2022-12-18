import json

from environs import Env
from google.cloud import dialogflow

env = Env()
env.read_env()
project_id = env('PROJECT_ID')


def create_intent(project_id):
    with open('../questions.json', 'r') as file:
        questions = file.read()

    raw_questions = json.loads(questions)

    client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    for questions_part, question_item in raw_questions.items():
        response_messages, callback_phrases = [], []

        for item in question_item['questions']:
            part = dialogflow.Intent.TrainingPhrase.Part(text=item)
            question = dialogflow.Intent.TrainingPhrase(parts=[part])
            callback_phrases.append(question)

        text = dialogflow.Intent.Message.Text(text=[question_item['answer']])
        message = dialogflow.Intent.Message(text=text)

        response_messages.append(message)

        display_name = '{}'.format(questions_part)
        intent = dialogflow.Intent(display_name=display_name, training_phrases=callback_phrases, messages=response_messages)

        client.create_intent(request={'parent': parent, 'intent': intent})


if __name__ == '__main__':
    create_intent(project_id)