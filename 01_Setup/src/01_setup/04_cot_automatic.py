import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are a helpful AI assistant that resolves user queries.
Break the problem into smaller steps and think through each one carefully.

Rules:
- Strictly follow the JSON output format
- Run one step at a time
- Follow the sequence of steps: Plan, then Output

Output format (JSON): { "step": "string", "content": "string" }

Input: what is 2+2*5/3
Output: { "step": "Plan", "content": "This is a mathematical expression, so I will use BODMAS." }
Output: { "step": "Plan", "content": "Multiplication first: 2*5 = 10, so the expression becomes 2+10/3." }
Output: { "step": "Plan", "content": "Next, division: 10/3 = 3.3333, so the expression becomes 2+3.3333." }
Output: { "step": "Plan", "content": "Finally, addition gives 5.3333." }
Output: { "step": "Output", "content": "5.3333" }
"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("👉 ")
message_history.append({"role":"user", "content":user_query})

while True:
    response = client.chat.completions.create(model="gpt-4o-mini",response_format={"type":"json_object"}, messages=message_history)

    raw_result = response.choices[0].message.content

    message_history.append({"role":"assistant", "content":raw_result})

    parsed_response = json.loads(raw_result)

    if parsed_response.get("step") == "Plan":
        print("🧠 Plan:", parsed_response.get("content"))
        message_history.append({ "role": "assistant", "content": "<>" })
        continue

    print("🤖:", parsed_response.get("content"))
    break


