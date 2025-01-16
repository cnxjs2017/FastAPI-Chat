import requests
import json

# 定义请求的URL
url = "http://10.202.94.52:20353/chat"

# 定义请求体
payload = {
    "model": "/groups/ai4legal/home/u12302024/LLaMA-Factory/models/Qwen2.5-7B-Instruct/Qwen2___5-7B-Instruct",
    "messages": [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": "你好呀"}
    ],
    # "temperature": 0.7,
    # "top_p": 0.8,
    # "max_tokens": 512,
    # "repetition_penalty": 1.05
}

# 设置请求头
headers = {
    "Content-Type": "application/json"
}

# 发送POST请求
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    print("Response from server:", response.json())
    ai_message = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    print(ai_message)
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"An error occurred: {err}")