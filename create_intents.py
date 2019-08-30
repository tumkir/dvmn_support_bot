import json
import os

import dialogflow_v2 as dialogflow
from dotenv import load_dotenv


def create_intent(intent_name, training_phrases_parts, message_texts, project_id):
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=intent_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)
    return response


if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv('project_id')

    with open('./questions.json') as questions_file:
        phrases = json.load(questions_file)

    for intent_name, data in phrases.items():
        questions = data['questions']
        answer = data['answer']
        create_intent(intent_name, questions, [answer], project_id=project_id)
