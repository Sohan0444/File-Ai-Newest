import os
import sys
from pathlib import Path

# Add the Backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from config import OPENAI_API_KEY
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o-mini",  # you can swap to "gpt-4.1" or others
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What’s the capital of France?"}
    ]
)

print(response.choices[0].message.content)