import json

from services.llm_client import client

def call_llm(prompt: str):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return json.loads(response.output_text)
