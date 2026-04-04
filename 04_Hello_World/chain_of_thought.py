from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()

#client = OpenAI(
#    api_key = getenv("GEMINI_API_KEY")
#    , base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
#)

client = OpenAI()


SYSTEM_PROMPT = """
    You're an expert Coding or Math ONLY Assistant in resolving user queries using chain of thought.
    The chain of thought shoudl be organized clearly, logically and step-wise using the following framework
       "USER INPUT" : you paraphrase and summarize the user problem as if you are thinking to yourself.
       "STEP" : [Can have multiple such STEP instances] You clearly state and describe the step down the path you are taking.
       "OUTPUT" :  You arrive at the result. start with the result statement and then give a short description if necessary.
    You need to first STEP what needs to be done. The STEP can be multiple instances.
    Once you think enough STEP has been done, you can produce an OUTPUT.

    Rules:
    - Strictly Follow the given JSON output format
    - Only give the output of one stage at a time. Don't give all steps at once. I'm internally calling you multiple times for the next stages while giving you the output of the previous stage as input
    - The sequence of Stage is USER INPUT (where user gives an input), STEP (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "Stage": "USER INPUT" | "STEP" | "OUTPUT", "content": "string" }

    Example:
    USER INPUT: Hey, Can you solve 2 + 3 * 5 / 10
    STEP: { "Stage": "USER INPUT": "content": "Seems like user is interested in math problem" }
    STEP: { "Stage": "STEP": "content": "looking at the problem, we should solve this using BODMAS method" }
    STEP: { "Stage": "STEP": "content": "Yes, The BODMAS is correct thing to be done here" }
    STEP: { "Stage": "STEP": "content": "first we must multiply 3 * 5 which is 15" }
    STEP: { "Stage": "STEP": "content": "Now the new equation is 2 + 15 / 10" }
    STEP: { "Stage": "STEP": "content": "We must perform divide that is 15 / 10  = 1.5" }
    STEP: { "Stage": "STEP": "content": "Now the new equation is 2 + 1.5" }
    STEP: { "Stage": "STEP": "content": "Now finally lets perform the add 3.5" }
    STEP: { "Stage": "STEP": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "Stage": "OUTPUT": "content": "3.5" }
    
"""
print("\n\n\n")

message_history = [
    {  
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

while True:
    user_query = input("Input >> ")
    if user_query == "exit":
        break

    message_history.append(
        {
                "role": "user",
                "content": user_query
        }
    )

    while True:
        response = client.chat.completions.create(
            model = "gpt-4o",
            response_format={"type": "json_object"},
            messages = message_history
        )

        raw_output = response.choices[0].message.content
        message_history.append(
            {
                "role": "assistant",
                "content": raw_output
        })
        
        
        parsed_result = json.loads(raw_output)

        if parsed_result.get("Stage") == "USER INPUT":
            print("🔥", parsed_result.get("content"))
            continue

        if parsed_result.get("Stage") == "STEP":
            print("🧠", parsed_result.get("content"))
            continue

        if parsed_result.get("Stage") == "OUTPUT":
            print("🤖", parsed_result.get("content"))
            break

    print("\n\n\n")
