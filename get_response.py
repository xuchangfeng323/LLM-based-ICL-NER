from openai import OpenAI
import os
from dotenv import load_dotenv



def get_deeppseek_response(model_name="deepseek-v4-flash", system_prompt="", user_prompt="" ):
    load_dotenv()
    client = OpenAI(
        api_key=os.environ["deepseek_api_key"],
        base_url="https://api.deepseek.com",
    )
    

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        response_format={
            'type': 'json_object'
        },
        top_p=1,
        temperature=1,
    )
    return response.choices[0].message.content
if __name__ == "__main__":
    get_deeppseek_response()