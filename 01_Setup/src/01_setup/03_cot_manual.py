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

message_history = [""]

responses = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is 2*4+6"},
        {"role": "assistant", "content": json.dumps({
            "step": "Plan",
            "content": "Alright! this looks like a mathematical equation that I need to solve."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "Plan",
            "content": "In order to solve this equation, I will have to use the BODMAS rule."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "Plan",
            "content": "According to BODMAS, we will perform multiplication and division from left to right before addition."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "Plan",
            "content": "First, I will calculate 2*4 = 8."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "Plan",
            "content": "Now the expression simplifies to 8+6."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "Plan",
            "content": "Lastly, I will perform the addition: 8 + 6 = 14."
        })},
        {"role": "assistant","content" : json.dumps({"step": "Output", "content": "14"})}
    ],
)

print(responses.choices[0].message.content)