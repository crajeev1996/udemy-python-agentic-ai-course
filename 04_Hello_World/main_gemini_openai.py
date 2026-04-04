from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

client = OpenAI(
    api_key = getenv("GEMINI_API_KEY")
    , base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "You are a manufacturing expert. Please only answer manufacturing questions in good detail. Politely refuse questions from any other subject area"
user_query = input("👉🏻 ")
response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {  
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
)

print(response.choices[0].message.content)