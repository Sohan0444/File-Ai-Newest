import os
import sys
from pathlib import Path

# Add the Backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import llm_parser

from config import OPENAI_API_KEY
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)




def determine_tools_from_query(query: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an ai file manager that can perform actions on files."},
            {"role": "user", "content": f"{llm_parser.send_tools_openai(query)}"}
        ]
    )
    print(response.choices[0].message.content)

