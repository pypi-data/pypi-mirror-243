import random
import uuid

from zmq_ai_client_python import LlamaClient
from zmq_ai_client_python.schema import Message, MessageRole, ChatCompletionRequest, ChatCompletion


def main():
    client = LlamaClient('tcp://localhost:5555', timeout=360000)

    user_uuid = uuid.UUID("708bab67-64d2-4e7d-94b6-2b6e043d880c")

    warmup_messages = [
        Message(role=MessageRole.system,
                content="A chat between a curious human and an artificial intelligence "
                        "assistant. The assistant gives helpful, detailed, and polite answers to the human's "
                        "questions."),
    ]

    followup_messages = [
        Message(role=MessageRole.user, content='What was the name of the city.'),
        Message(role=MessageRole.user, content='What was the name of the country that I asked?'),
        Message(role=MessageRole.user, content=f'Tell me more about the capital of the country?'),
        Message(role=MessageRole.user, content=f'What is the population of the city in your answer?'),
        Message(role=MessageRole.user, content=f'What is the population of the country in the context?'),
        Message(role=MessageRole.user, content=f'What is the area of the country?')
    ]

    countries = ["Germany", "Italy", "Spain", "Netherlands", "Switzerland", "Denmark", "Sweden", "Poland",
                 "Czech Republic", "Greece", "Bulgaria", "Romania", "Ukraine", "United Kingdom"]

    STOP = ["\n### Human:"]

    session_countries = {}

    # send initial messages for each session
    for _ in range(10):
        country_index = random.randint(0, len(countries) - 1)
        country = countries[country_index]

        messages = warmup_messages + [
            Message(role=MessageRole.user, content=f'What is the capital of {country}?')
        ]

        request = ChatCompletionRequest(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.8,
            n=2048,
            stop=STOP,
            user=user_uuid,
        )

        print(f"** Question: {messages[len(warmup_messages)].content}'")

        response: ChatCompletion = client.send_chat_completion_request(request)
        session_uuid = response.key_values["session"]
        session_countries[session_uuid] = country

        print(f"=== Session {session_uuid} is about {country} ===")
        answer = response.choices[0].message.content

        print(f"## Answer: {answer}")

    # send each followup messages for each session
    for message in followup_messages:
        for session_uuid, country in session_countries.items():

            request = ChatCompletionRequest(
                model='gpt-3.5-turbo',
                messages=[message],
                temperature=0.8,
                n=1024,
                stop=STOP,
                user=user_uuid,
                key_values={"session": session_uuid}
            )

            print(f"=== Session {session_uuid} is about {country} ===")
            print(f"** Question: {message.content}'")

            response: ChatCompletion = client.send_chat_completion_request(request)

            answer = response.choices[0].message.content
            print(f"## Answer: {answer}")


if __name__ == "__main__":
    main()
