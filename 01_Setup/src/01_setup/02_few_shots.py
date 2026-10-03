from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

####
# WHEN WE INCLUDE FORMAT LIKE THIS

responses = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role":"user",
        "content":
        """"
        1. What is 2 plus 2?
        2. What is 5+6?
        3. What is three plus 8?
        Do not add anything else in the answer just return the value as is, follow the example
        Examples: 
        1. What is 2+4?  
        Expected output : 6
        2. 2 plus 8?
        Expected output : 10 
            
        """

        
    }]
)

print(responses.choices[0].message.content)



