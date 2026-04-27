import requests
from app.config import Config

def generate_from_llm(prompt: str):
    response = requests.post(
        f"{Config.BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {Config.LLM_TOKEN}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Question Generator"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code != 200:
        raise Exception(f"LLM request failed: {response.status_code} - {response.text}")

    return response.json()
