from micInput import *
from weather import *
from openai import OpenAI
from dotenv import load_dotenv
import json


load_dotenv()
client = OpenAI()

'''
"root": {
    "type": "object",
    "description": "The tKinter object that holds the Graphical User Interface Window."
},
"name": {
    "type": "string",
    "description": "The name of the user currently using the application."
}
'''
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
    },
    {
        "type": "function",
        "function":{
            "name": "switch_to_maps",
            "description": "Switches / Goes to the Maps. Shows the user the map page.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": [
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "switch_to_calendar",
            "description": "Switches / Goes to the Calendar. Shows the user their calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": [
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "switch_to_remin",
            "description": "Switches / Goes to the Reminders page. Shows the user their reminders.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": [
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "switch_to_main_ui",
            "description": "Switches / Goes to the main UI page. Shows the user the main UI page.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": [
                ]
            }
        }
    }
]
def askGPT(command):
    from MainUI import sharedqueue, switch_to_maps, switch_to_calendar, switch_to_remin
    from maps import switch_to_main_ui #as maps_to_main
    #from calendar import switch_to_main_ui as calendar_to_main

    available_functions = {
        "getCurrentWeather": getCurrentWeather,
        "switch_to_maps": switch_to_maps,
        "switch_to_calendar": switch_to_calendar,
        "switch_to_remin": switch_to_remin,
        "switch_to_main_ui": switch_to_main_ui,
    }
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
            elif(function_to_call == switch_to_maps):
                cock = sharedqueue.get()
                function_response = function_to_call(cock[0], cock[1], cock[2])
                return "switched"
            elif(function_to_call == switch_to_calendar):
                cock = sharedqueue.get()
                function_response = function_to_call(cock[0], cock[1], cock[2])
                return "switched"
            elif(function_to_call == switch_to_remin):
                cock = sharedqueue.get()
                function_response = function_to_call(cock[0], cock[1], cock[2])
                return "switched"
            elif(function_to_call == switch_to_main_ui):
                cock = sharedqueue.get()
                function_response = function_to_call(cock[0], cock[1], cock[2])
                return "switched"
                '''if(cock[0].title == "Maps"):
                    function_response = maps.function_to_call(cock[0], cock[1], cock[2])'''
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
    else:
        return response_message.content

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