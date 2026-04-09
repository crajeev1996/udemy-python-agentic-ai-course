from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
import json

import requests

load_dotenv()

def get_weather():
    city = input('city:')
    url = f'http://api.weatherapi.com/v1/current.json?key={getenv('WEATHERAPI_API_KEY')}&q={city}'
    response = requests.get(url)
    response_parsed = response.json()

    if response.status_code == 200:
        return f"The weather in {response_parsed['location']['name']}, {response_parsed['location']['country']} is {response_parsed['current']['temp_c']} C with conditions {response_parsed['current']['condition']['text']}"
    
    return 'API call failed'



client = OpenAI()

def main():
    while True:
        user_query = input("Chat>>")
        if user_query == 'exit':
            break
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = [
                {"role" : "user", "content": user_query}
            ]
        )

        print(f"ChatGPT: {response.choices[0].message.content}")

    print("Program succesfully exited...")

    return

print(get_weather())

#main()