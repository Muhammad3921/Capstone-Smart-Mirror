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
    },
    {
        "type": "function",
        "function":{
            "name": "add_task",
            "description": "Adds a task or reminder to the user's reminders. Used when the user wants to reminded of something. Confirm the user's request at the end.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task or reminder to be added to the user's list of reminders."
                    }
                },
                "required": [
                    "task"
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "complete_task",
            "description": "Removes a completed task from the list of reminders. Call this whenever a user says they have completed a task. Confirm the user's request at the end.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task or reminder that was completed from the user's list of reminders."
                    }
                },
                "required": [
                    "task"
                ]
            }
        }
    }
]
def askGPT(command):
    from MainUI import sharedqueue, switch_to_maps, switch_to_calendar, switch_to_remin
    from maps import switch_to_main_ui #as maps_to_main
    #from calendar import switch_to_main_ui as calendar_to_main
    from reminder import add_task, complete_task

    available_functions = {
        "getCurrentWeather": getCurrentWeather,
        "switch_to_maps": switch_to_maps,
        "switch_to_calendar": switch_to_calendar,
        "switch_to_remin": switch_to_remin,
        "switch_to_main_ui": switch_to_main_ui,
        "add_task": add_task,
        "complete_task": complete_task
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
            elif(function_to_call == add_task):
                cock = sharedqueue.get()
                sharedqueue.put(cock)
                function_response = function_to_call(task = function_parameters.get("task"), name = cock[2])
            elif(function_to_call == complete_task):
                from reminder import incomplete_tasks
                tasks = ", ".join(str(elem) for elem in incomplete_tasks)
                messages_t = [{
                    "role": "assistant",
                    "content": "Return the task, from the list of tasks, that is closest to the prompt. You should return the exact string of the task chosen. List of tasks: " + tasks + ". Prompt: " + function_parameters.get("task")
                }]

                task = client.chat.completions.create(
                    model="gpt-3.5-turbo-0613",
                    messages=messages_t
                ).choices[0].message.content
                cock = sharedqueue.get()
                sharedqueue.put(cock)
                function_response = function_to_call(task = task, username = cock[2])

            #GPT's response to the request, not the function's return
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