import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()  # OPENAI_API_KEY 필요

response = client.responses.create(
    model="gpt-4o",
    input="OpenAI 를 한 문장으로 설명해 줘"
)

print('😎', response.output_text)



