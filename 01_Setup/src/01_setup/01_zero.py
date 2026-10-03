from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

responses = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role":"user",
        "content":""""
            what is 2+2?
        """
    }]
)

print(responses.choices[0].message.content)

# this is the output if we do not define any format
# (01-setup) ➜  01_setup git:(master) ✗ python3 02_few_shots.py
# 2 + 2 = 4.
# (01-setup) ➜  01_setup git:(master) ✗ python3 02_few_shots.py
# 2 + 2 equals 4.

