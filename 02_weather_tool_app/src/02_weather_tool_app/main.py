from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def main():
    user_input = input("> ")
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[
        {"role":"user", "content":user_input}
    ])

    print(f"{response.choices[0].message.content}")

print(get_weather("pune"))
main()