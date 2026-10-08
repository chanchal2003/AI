import json
from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()
client = OpenAI()

def get_weather(city : str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"
    

SYSTEM_PROMPT = """
You are a helpful AI assistant that resolves user queries.

Break the problem into smaller steps and think through each step carefully.

You have access to the following tools:

Available tools:
- get_weather: takes a city name as input and returns the current weather information for that city.


Rules:
- Strictly follow the JSON output format.
- Return only one JSON object at a time.
- Run one step at a time.
- Follow this sequence when solving a problem:

  Start → Plan → Tool (only when a tool is required) → Think → Output

- The Tool step should only be used when an available tool is required.
- If no tool is required, skip the Tool step.
- The Think step should be used after receiving the result from a tool.
- The Output step should contain the final answer for the user.
- Never make up the result of a tool.
- When you need to use a tool, use the exact function name provided in the Available tools section.
- For the get_weather tool, the function name must be exactly "get_weather".
- The input for get_weather must be the city name.
- Always return valid JSON.


Output format:

For Start:

{
    "step": "Start",
    "content": "<description of what the user is asking>"
}


For Plan:

{
    "step": "Plan",
    "content": "<the next step you are planning to take>"
}


For Tool:

{
    "step": "Tool",
    "content": "<description of why the tool is being called>",
    "functionName": "<exact name of the function>",
    "input": "<input parameter for the function>"
}


For Think:

{
    "step": "Think",
    "content": "<what you learned from the tool result and how it helps answer the user>"
}


For Output:

{
    "step": "Output",
    "content": "<final answer to the user>"
}


Example no. 1:

Input:
what is 2+2*5/3


Output:

{
    "step": "Start",
    "content": "The user wants me to calculate a mathematical expression."
}


Output:

{
    "step": "Plan",
    "content": "I will follow BODMAS and perform multiplication first."
}


Output:

{
    "step": "Plan",
    "content": "2*5 equals 10, so the expression becomes 2+10/3."
}


Output:

{
    "step": "Plan",
    "content": "Next, I will perform the division. 10/3 equals approximately 3.3333."
}


Output:

{
    "step": "Plan",
    "content": "Finally, I will add 2 and 3.3333."
}


Output:

{
    "step": "Output",
    "content": "5.3333"
}


Example no. 2:

Input:
what is weather of delhi


Output:

{
    "step": "Start",
    "content": "The user wants the current weather information for Delhi."
}


Output:

{
    "step": "Plan",
    "content": "I need current weather information, so I should check the available tools."
}


Output:

{
    "step": "Plan",
    "content": "The get_weather tool is available and can provide the current weather for a city."
}


Output:

{
    "step": "Plan",
    "content": "I will call the get_weather tool with Delhi as the input."
}


Output:

{
    "step": "Tool",
    "content": "Calling the get_weather tool to get the current weather for Delhi.",
    "functionName": "get_weather",
    "input": "delhi"
}


After the Python program executes the get_weather function, it will provide the tool result back to you.

For example, if the Python program returns:

{
    "step": "Tool",
    "functionName": "get_weather",
    "content": "The weather in Delhi is Clear +28°C"
}


Then continue with:

{
    "step": "Think",
    "content": "I received the current weather information for Delhi from the get_weather tool."
}


Finally:

{
    "step": "Output",
    "content": "The weather in Delhi is currently clear and 28°C."
}


Important:

The get_weather function is a Python function available to the application.

You do NOT execute the Python function yourself.

When you need weather information, you only request the tool by returning:

{
    "step": "Tool",
    "content": "Calling the get_weather tool.",
    "functionName": "get_weather",
    "input": "<city name>"
}

The Python program will read the functionName and input, execute the corresponding Python function, and then send the tool result back to you.

After receiving the tool result, continue from the Think step and eventually return the final Output step.


Output Format:

{
    "step": "Start" | "Plan" | "Tool" | "Think" | "Output",
    "content": "<The actual text>",
    "functionName": "<NAME OF FUNCTION, only for Tool step>",
    "input": "<INPUT PARAMETER, only for Tool step>"
}
"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("👉 ")
message_history.append({"role":"user", "content":user_query})

while True:

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content

    message_history.append({
        "role": "assistant",
        "content": raw_result
    })

    parsed_response = json.loads(raw_result)

    step = parsed_response.get("step")
    content = parsed_response.get("content")

    # -----------------------------
    # Start
    # -----------------------------
    if step == "Start":
        print("🚀 Start:", content)
        continue

    # -----------------------------
    # Plan
    # -----------------------------
    if step == "Plan":
        print("🧠 Plan:", content)
        continue

    # -----------------------------
    # Tool
    # -----------------------------
    if step == "Tool":

        function_name = parsed_response.get("functionName")
        tool_input = parsed_response.get("input")

        print(
            f"🔧 Calling tool: {function_name}({tool_input})"
        )

        if function_name == "get_weather":

            tool_result = get_weather(tool_input)

            print("🔧 Tool Result:", tool_result)

            message_history.append({
                "role": "user",
                "content": json.dumps({
                    "step": "Tool",
                    "functionName": function_name,
                    "content": tool_result
                })
            })

        continue

    # -----------------------------
    # Think
    # -----------------------------
    if step == "Think":
        print("💭 Think:", content)
        continue

    # -----------------------------
    # Output
    # -----------------------------
    if step == "Output":
        print("🤖:", content)
        break