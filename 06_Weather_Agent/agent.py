from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
import json
import requests

load_dotenv()

#client = OpenAI(
#    api_key = getenv("GEMINI_API_KEY")
#    , base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
#)

client = OpenAI()

def get_weather(city:str):
    url = f'http://api.weatherapi.com/v1/current.json?key={getenv('WEATHERAPI_API_KEY')}&q={city}'
    response = requests.get(url)
    response_parsed = response.json()

    if response.status_code == 200:
        return f"The weather in {response_parsed['location']['name']}, {response_parsed['location']['country']} is {response_parsed['current']['temp_c']} C with conditions {response_parsed['current']['condition']['text']}"
    
    return 'API call failed'

available_tools = {
    "get_weather": get_weather
}


SYSTEM_PROMPT = """
    You're an expert Weather or Math ONLY agent Assistant in resolving user queries using chain of thought.
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
    - You may also call a tool if available from the list of available toolsto give better quality answers
    - If the user query is triaged as weather query, wait for OBSERVE step which is the output from the called tool 

    Output JSON Format:
    { "Stage": "USER INPUT" | "STEP" | "OUTPUT" | "TOOL"
    , "content" : "string"
    , "tool" : "string" | None
    , "input" : "string" | None}

    Available Tools:
    - get_weather: Takes city name as input. If city name is ambiguous i.e, more than 1 city with same name, it can also take same input in the form [city],[country]. Returns a 1 line string weather info about the city.

    Example 1:
    USER INPUT: Hey, Can you solve 2 + 3 * 5 / 10
    STEP: { "Stage": "USER INPUT", "content": "Seems like user is interested in math problem" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "looking at the problem, we should solve this using BODMAS method" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Yes, The BODMAS is correct thing to be done here" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "first we must multiply 3 * 5 which is 15" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Now the new equation is 2 + 15 / 10" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "We must perform divide that is 15 / 10  = 1.5" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Now the new equation is 2 + 1.5" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Now finally lets perform the add 3.5" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "Stage": "OUTPUT": "content": "3.5" }

    Example 2:
    USER INPUT: Hey, What's the weather in Delhi?
    STEP: { "Stage": "USER INPUT", "tool" : None , "input" : None, "content": "Seems like user wants to know current weather information" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Are there multiple Delhi's in the world" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "There's 1 in Canada and 1 in India" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "But the 1 in India is most famous / populous" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Since I cannot check current weather information, let me check if there are any available tools. hey, I'm an agent now! " }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Found it! There is a get_weather tool available" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "The input to this tool needs to be 'Delhi, India' as there are multiple cities with the same name and I am assuming the user is asking weather information for the most famous instance" }
    STEP: { "Stage": "TOOL", "tool": "get_weather", "input": "Delhi, India", "content": "I have determined the tool and the input string for the API call" }
    STEP: { "Stage": "OBSERVE", "tool" : None , "input" : None, "content": "The weather in Delhi, India is 11 C with conditions patchy rain" }
    STEP: { "Stage": "STEP", "tool" : None , "input" : None, "content": "Great! The output is along expected lines and the API call worked" }
    OUTPUT: { "Stage": "OUTPUT", "tool" : None , "input" : None, "content": "The current weather in Delhi, India is 11 C with conditions patchy rain" }
    
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

        if parsed_result.get("Stage") == "TOOL":
            tool_to_call = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f"TOOL: {tool_to_call}({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"TOOL: {tool_to_call}({tool_input}) = {tool_response}")
            message_history.append({"role": "developer", "content":json.dumps(
                {"step": "OBSERVE", "tool" : tool_to_call, "input": tool_input, "output":tool_response}
            )})
            continue

        if parsed_result.get("Stage") == "OUTPUT":
            print("🤖", parsed_result.get("content"))
            break

    print("\n\n\n")
