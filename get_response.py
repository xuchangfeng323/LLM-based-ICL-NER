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
        extra_body={"thinking": {"type": "disabled"}}
    )
    return response.choices[0].message.content
def get_gpt_response(model_name="gpt-5.6-luna", system_prompt="", user_prompt="" ):
    load_dotenv()
    client = OpenAI(
        api_key=os.environ["gpt_api_key"],
        base_url="https://zyapi.tuluo.top:8888/v1",
    )
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        top_p=1,
        temperature=1,
        extra_body={"thinking": {"type": "disabled"}}
    )
    return response.choices[0].message.content
def get_qwen_response(model_name="Qwen3.6-35B-A3B-abliterated", system_prompt="", user_prompt="" ):
    load_dotenv()
    client = OpenAI(
        api_key=os.environ["api_key"],
        base_url="https://zyapi.tuluo.top:8888/v1",
    )
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        top_p=1,
        temperature=1,
        extra_body={
        "enable_thinking": False,
        },
    )
    return response.choices[0].message.content
if __name__ == "__main__":
    get_deeppseek_response()