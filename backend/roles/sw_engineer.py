import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle(input_data: str) -> str:
    prompt = f"You are a senior software engineer. Help with:\n\n{input_data}"
    response = client.chat.completions.create(
        model="gpt-4-code",  # or "gpt-4o" if unavailable
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content