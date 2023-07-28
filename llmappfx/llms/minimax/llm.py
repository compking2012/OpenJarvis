import requests
import json

class llm:
    def __init__(self):
        llmconfig = read_json_file("llmconfig.json")

        group_id = llmconfig["group_id"]
        api_key = llmconfig["api_key"]
        api_url = llmconfig["api_url"]
        self.url = f"{api_url}{group_id}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.payload = {
            "model": "abab5.5-chat",
            "tokens_to_generate": 256,
            "temperature": 0.9,
            "top_p": 0.95,
            "stream": False,
            "role_meta": {
                "user_name": "用户",
                "bot_name": "MM智能助理"
            },
            "prompt": "{instruction}",
            "messages": [
                {
                "sender_type": "USER",
                "text": "{question}"
                }
            ]
        }

    def read_json_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    def set_instruction(self, instruction):
        self.instruction = instruction

    def get_answer(self, question):
        json = self.payload.replace("{instruction}", self.instruction).replace("{question}", question)
        response = requests.post(self.url, headers=self.headers, json=json)

        print(response.status_code)
        print(response.text)
        return response.text