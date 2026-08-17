from openai import OpenAI
import os
from dotenv import load_dotenv
import ollama
from ollama import Client, ChatResponse


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
if "api_key"  in os.environ:
    client = OpenAI(
        api_key=os.environ["api_key"],
        base_url="https://zyapi.tuluo.top:8888/v1",
    )
ollama_client = Client(host="http://localhost:11434")
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
def get_ollama_response(model_name="qwen3.8", system_prompt="", user_prompt="" ):
    model_list=[m.model for m in ollama.list().models]
    if model_name not in model_list:
        model_name="qwen3.8"
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response:ChatResponse = ollama_client.chat(
        model=model_name,
        messages=messages,
        think=False,
        options={
            "temperature": 1,
            "top_p": 1,
        }
    )
    return response.message.content
def get_mimo_response(model_name="mimo-v2.5", system_prompt="", user_prompt="" ):
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
if __name__ == "__main__":
    print(get_ollama_response("qwen3.8", "你", "你好"))
    