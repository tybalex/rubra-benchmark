import json
import uuid


def add(args: str):
    args = json.loads(args)
    try:
        return str(float(args["a"]) + float(args["b"]))
    except Exception as e:
        return f"Error: e"


def sub(args: str):
    args = json.loads(args)
    try:
        return str(float(args["a"]) - float(args["b"]))
    except Exception as e:
            return f"Error: e"


def mult(args: str):
    args = json.loads(args)
    try:
        
        return str(float(args["a"]) * float(args["b"]))
    except Exception as e:
        return f"Error: e"


def div(args: str):
    args = json.loads(args)
    try:
        
        return str(float(args["a"]) / float(args["b"]))
    except Exception as e:
        return f"Error: e"


def get_oai_response(model, functions, msgs, api_key, base_url):
  import openai
  openai.api_key = api_key ## Add your API key here
  openai.base_url = base_url
  
  
  try:
    completion = openai.chat.completions.create(
      model=model,
      temperature=0.1,
      messages=msgs,
      tools=functions,
      tool_choice="auto",
      # functions=functions,
      # function_call="auto",
      stream=False,
    )
    return completion.choices[0]
  except Exception as e:
    print(e)



def insert_tool_response(res, msgs):

    assistant_message = res.message
    tool_calls = []
    for tool_call in assistant_message.tool_calls:
        tool_calls.append( {
                            "id": tool_call.id,
                            "function": {"name": tool_call.function.name,
                                        "arguments": tool_call.function.arguments},
                            "type": "function",
                        })
    msgs.append({"role": "assistant",  "tool_calls": tool_calls})
    
    for i, tool_call in enumerate(assistant_message.tool_calls):
        if tool_call.function.name == "getCurrentWeather":
            l = len((json.loads(assistant_message.tool_calls[i].function.arguments))["location"])
            msgs.append({"role": "tool", "tool_call_id": str(assistant_message.tool_calls[i].id), "name": assistant_message.tool_calls[i].function.name, "content": f"temprature is {(i+1) * 50 + l } degree"})
        elif tool_call.function.name == "calculate_distance":
            msgs.append({"role": "tool", "tool_call_id": str(assistant_message.tool_calls[i].id), "name": assistant_message.tool_calls[i].function.name, "content": f"Distance is {(i+1) * 50} miles."})
        elif tool_call.function.name == "generate_password":
            msgs.append({"role": "tool", "tool_call_id": str(assistant_message.tool_calls[i].id), "name": assistant_message.tool_calls[i].function.name, "content": f"Password generated: {uuid.uuid4().hex[:8]}"})
        elif tool_call.function.name == "orderUmbrella":
            msgs.append({"role": "tool", "tool_call_id": str(assistant_message.tool_calls[i].id), "name": assistant_message.tool_calls[i].function.name, "content": f"Order placed. the price is {(i+1) * 10} dollars."})
        elif tool_call.function.name == "list_files":
            msgs.append({"role": "tool", "tool_call_id": str(assistant_message.tool_calls[i].id), "name": assistant_message.tool_calls[i].function.name, "content": f"File list:\nreport.docx\ntask.txt\nnotes.txt"})
        elif tool_call.function.name == "get_file_size":
            msgs.append({"role": "tool", "tool_call_id": str(assistant_message.tool_calls[i].id), "name": assistant_message.tool_calls[i].function.name, "content": f"the size is {(i+1) * 100} bytes."})
        elif tool_call.function.name == "addition":
            msgs.append({
                "role": "tool",
                "name": "addition",
                "content": add(tool_call.function.arguments),
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "subtraction":
            msgs.append({
                "role": "tool",
                "name": "subtraction",
                "content": sub(tool_call.function.arguments),
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "multiplication":
            msgs.append({
                "role": "tool",
                "name": "multiplication",
                "content": mult(tool_call.function.arguments),
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "division":
            msgs.append({
                "role": "tool",
                "name": "division",
                "content": div(tool_call.function.arguments),
                "tool_call_id": tool_call.id
            })
        # print(f"Observation: {msgs[-1]}")
    
    return msgs

functions = [
        # {"type": "function","function":{"name":"calculate_distance","description":"Calculate the distance between two locations","parameters":{"type":"object","properties":{"origin":{"type":"string","description":"The starting location"},"destination":{"type":"string","description":"The destination location"},"mode":{"type":"string","description":"The mode of transportation"}},"required":["origin","destination","mode"]}}},{"type": "function","function":{"name":"generate_password","description":"Generate a random password","parameters":{"type":"object","properties":{"length":{"type":"integer","description":"The length of the password"}},"required":["length"]}}},
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "List all files in a directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "the directory to list files from"
                        }
                    },
                    "required": [
                        "directory"
                    ]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "description": "Create a 3D model of an object with specified dimensions",
                "name": "create_3d_model",
                "parameters": {
                    "properties": {
                    "object_name": {
                        "description": "Name of the object to be modeled",
                        "type": "string"
                    },
                    "dimensions": {
                        "description": "Dimensions of the 3D object (length, width, height)",
                        "type": "object",
                        "properties": {
                        "length": {
                            "type": "number"
                        },
                        "width": {
                            "type": "number"
                        },
                        "height": {
                            "type": "number"
                        }
                        },
                        "required": [
                        "length",
                        "width",
                        "height"
                        ]
                    }
                    },
                    "required": [
                    "object_name",
                    "dimensions"
                    ],
                    "type": "object"
                }
            }
        },
        {
            "type": "function",
            "function": {
                "description": "Get the latest insurance premium from a list of premiums.",
                "name": "latest_insurance_premium",
                "parameters": {
                    "properties": {
                        "premiums": {
                            "description": "List of insurance premiums",
                            "type": "array",
                            "items": {
                            "type": "number"
                            }
                        }
                    },
                    "required": [
                        "premiums"
                    ],
                    "type": "object"
                }
            }
        },
        {
            "type": "function",
            "function": {
            "description": "Calculate insurance premium based on age and coverage",
            "name": "calculate_insurance_premium",
            "parameters": {
                "properties": {
                "age": {
                    "description": "Age of the person applying for insurance",
                    "type": "integer"
                },
                "coverage_type": {
                    "description": "Type of insurance coverage",
                    "type": "string",
                    "enum": [
                    "basic",
                    "standard",
                    "premium"
                    ]
                }
                },
                "required": [
                "age",
                "coverage_type"
                ],
                "type": "object"
            }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_file_size",
                "description": "Get the size of a file in bytes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "the name of the file to get its size"
                        }
                    },
                    "required": [
                        "filename"
                    ]
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'addition',
                'description': "Adds two numbers together",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to add',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Second number to add',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'subtraction',
                'description': "Subtracts two numbers",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to be subtracted from',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Number to subtract',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'multiplication',
                'description': "Multiply two numbers together",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to multiply',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Second number to multiply',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'division',
                'description': "Divide two numbers",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to use as the dividend',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Second number to use as the divisor',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
      {
          "type": "function",
        "function": {
          "name": "getCurrentWeather",
          "description": "Get the weather in location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
              "unit": {"type": "string", "enum": ["c", "f"]}
            },
            "required": ["location"]
          }
        }
      },
      {    "type": "function",
        "function":
        {
            "name": "orderUmbrella",
            "description": "Do this to help user to order an umbrella online", 
            "parameters": {
                "type": "object",
                "properties": {
                    "number_to_buy": {
                        "type": "integer",
                        "description": "the amount of umbrellas to buy"
                    }
                },
                "required": [
                    "number_to_buy"
                ]
            }
        }},
      {
        "type": "function",
        "function": {
          "name": "k8sAgent",
          "description": "An agent that can help you with your kubernetes cluster by executing kubectl commands",
          "parameters": {
            "properties": {
              "task": {
                "description": "The kubectl releated task to accomplish",
                "type": "string"
              }
            },
            "type": "object"
          }
        }
      },
      {
        "type": "function",
        "function": {
          "name": "exec",
          "description": "Execute a command and get the output of the command",
          "parameters": {
            "properties": {
              "command": {
                "description": "The command to run including all applicable arguments",
                "type": "string"
              },
              "directory": {
                "description": "The directory to use as the current working directory of the command. The current directory \".\" will be used if no argument is passed",
                "type": "string"
              }
            },
            "type": "object"
          }
        }
      },
    
      {"type": "function","function":{"name":"calculate_distance","description":"Calculate the distance between two locations","parameters":{"type":"object","properties":{"origin":{"type":"string","description":"The starting location"},"destination":{"type":"string","description":"The destination location"},"mode":{"type":"string","description":"The mode of transportation"}},"required":["origin","destination","mode"]}}},{"type": "function","function":{"name":"generate_password","description":"Generate a random password","parameters":{"type":"object","properties":{"length":{"type":"integer","description":"The length of the password"}},"required":["length"]}}}
       ]

def run_completion(chat_method, user_query, msgs=[], model="gpt-4-0125-preview"):
    system_prompt = "You are a helpful assistant."
    
    # functions = [{"type": "function","function":{"name":"calculate_distance","description":"Calculate the distance between two locations","parameters":{"type":"object","properties":{"origin":{"type":"string","description":"The starting location"},"destination":{"type":"string","description":"The destination location"},"mode":{"type":"string","description":"The mode of transportation"}},"required":["origin","destination","mode"]}}},{"type": "function","function":{"name":"generate_password","description":"Generate a random password","parameters":{"type":"object","properties":{"length":{"type":"integer","description":"The length of the password"}},"required":["length"]}}}]

    if not msgs or len(msgs) == 0:
        msgs = [{"role": "system", "content":system_prompt} ,{"role": "user", "content": user_query}]
    else:
        msgs.append({"role": "user", "content": user_query})

    res = chat_method(model=model, functions=functions, msgs=msgs)
    res_next = res
    l = 0
    while res_next.message.tool_calls and len(res_next.message.tool_calls) > 0:
        msgs = insert_tool_response(res_next, msgs)
        res_next = chat_method(model=model, functions=functions, msgs=msgs)
        l += 1
        if l > 5: # likely in a unnecessary dead loop
            break
    
    msgs.append({"role": "assistant", "content": res_next.message.content})
    return msgs