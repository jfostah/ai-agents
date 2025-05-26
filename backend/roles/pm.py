from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_pm_output(name: str, idea: str, target_users: str) -> dict:
    prompt = f"""
    You are a product manager AI. Help create a product plan for startup:
    Name: {name}
    Idea: {idea}
    Target Users: {target_users}

    Provide a markdown formatted output.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    markdown_output = response.choices[0].message.content
    return {"markdown_output": markdown_output}