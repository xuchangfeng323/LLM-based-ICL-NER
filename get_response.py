from openai import OpenAI
import os
from dotenv import load_dotenv



def get_deeppseek_response():
    load_dotenv()
    client = OpenAI(
        api_key=os.environ["deepseek_api_key"],
        base_url="https://api.deepseek.com",
    )
    system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""
    user_prompt = "Which is the longest river in the world? The Nile River."

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    print(response.choices[0].message.content)
if __name__ == "__main__":
    get_deeppseek_response()