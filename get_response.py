from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
if "deepseek_api_key"  in os.environ:
    deepseek_client = OpenAI(
        api_key=os.environ["deepseek_api_key"],
        base_url="https://api.deepseek.com",
    )
if "gpt_api_key"  in os.environ:
    gpt_client = OpenAI(
        api_key=os.environ["gpt_api_key"],
        base_url="https://zyapi.tuluo.top:8888/v1",
    )
if "qwen_api_key"  in os.environ:
    qwen_client = OpenAI(
        api_key=os.environ["qwen_api_key"],
        base_url="https://zyapi.tuluo.top:8888/v1",
    )
def get_deepseek_response(model_name="deepseek-v4-flash", system_prompt="", user_prompt="" ):
    
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = deepseek_client.chat.completions.create(
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
    
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = gpt_client.chat.completions.create(
        model=model_name,
        messages=messages,
        top_p=1,
        temperature=1,
        extra_body={"thinking": {"type": "disabled"}}
    )
    return response.choices[0].message.content
def get_qwen_response(model_name="Qwen3.6-35B-A3B-abliterated", system_prompt="", user_prompt="" ):
    
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = qwen_client.chat.completions.create(
        model=model_name,
        messages=messages,
        top_p=1,
        temperature=1,
        extra_body={
        "enable_thinking": False,
        },
    )
    return response.choices[0].message.content
