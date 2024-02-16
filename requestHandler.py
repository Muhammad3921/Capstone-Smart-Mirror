from micInput import *
from weather import *
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

available_functions = {
    "getCurrentWeather": getCurrentWeather,

}
tools = [
    {
        "type": "function",
        "function":{
            "name": "getCurrentWeather",
            "description": "Gets the current weather condition based on a location",
            "parameters": {
                "type": "object",
                "properties": {
                "location": {
                    "type": "string",
                    "description": "The location in which to get weather conditions on"
                }
                },
                "required": [
                    "location"
                ]
            }
        }
    }
]
def askGPT(command):
    
    messages = [{"role": "user", "content": command}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    #print(response)
    #print("****************")
    response_message = response.choices[0].message
    #print(response_message)
    tool_calls = response_message.tool_calls

    if(tool_calls):
        messages.append(response_message)

        for f in tool_calls:
            function_to_call = available_functions[f.function.name]
            function_parameters = json.loads(f.function.arguments)
            function_response = None

            if(function_to_call == getCurrentWeather):
                function_response = function_to_call(location=function_parameters.get("location"))
                

            messages.append(
                {
                    "tool_call_id": f.id,
                    "role": "tool",
                    "name": f.function.name,
                    "content": function_response
                }
            )

            response_to_user = client.chat.completions.create(
                model="gpt-3.5-turbo-0613",
                messages=messages
            )
    return response_to_user.choices[0].message.content

def startMirror():
    while True:
        print("Listening for keyword")
        if(listen()):
            getVoiceCommand()
            command = transcribeCommand()["text"]
            print("Transcripted command: " + command)

            if("bye" in command.lower()):
                print("Goodbye sire")
                break
            else:
                print("GPT response to user: " + askGPT(command))