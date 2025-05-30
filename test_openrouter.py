from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Say hello!"},
            {"role": "user", "content": "Test"}
        ],
        max_tokens=10
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")