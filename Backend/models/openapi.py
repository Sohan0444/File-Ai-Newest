import sys
import os

# Add the parent directory to the path so we can import from Backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import OPENAI_API_KEY
    from openai import OpenAI
    
    print("✅ Successfully imported OpenAI API key")
    print(f"API Key loaded: {OPENAI_API_KEY[:20]}...")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("✅ OpenAI client created successfully")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "What is the latest news in technology?"},
        ],
        max_tokens=200  # 🚀 hard cap on output length
    )
    
    print("✅ API call successful!")
    print("Response:")
    print(response.choices[0].message.content)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the Backend directory")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check your API key and internet connection")