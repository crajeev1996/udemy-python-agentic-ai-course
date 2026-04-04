from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

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

main()