#!/usr/bin/env python3

import os, json, dotenv, requests
from datetime import datetime

dotenv.load_dotenv()

class TextMessage:
    
    ROLE_AI = "assistant"
    ROLE_USER = "user"
    ROLE_SYSTEM = "system"
    
    def __init__(self, role, message):
        self.role = role
        self.message = message
    
    def getData(self):
        return {
            "role": self.role,
            "content": self.message
        }
    
class Context:
    
    def __init__(self):
        self.items = []
    
    def add(self, message):
        self.items.append(message)
    
    def getData(self):
        items = [item.getData() for item in self.items]
        return items

class Provider:
    
    def getModelName(self):
        return ""
    
    def getUrl(self):
        return ""
    
    def getApiKey(self):
        return ""

class OpenRouter(Provider):
    
    def __init__(self, model_name=""):
        super().__init__()
        self.model_name = model_name
    
    def getModelName(self):
        return self.model_name
    
    def getUrl(self):
        return "https://openrouter.ai/api/v1/chat/completions"
    
    def getApiKey(self):
        return os.getenv("OPENROUTER_API_KEY")

def send_llm(provider, prompt):
    
    data = {
        "model": provider.getModelName(),
        "messages": prompt.getData(),
    }
    
    headers = {
        "Authorization": "Bearer " + provider.getApiKey()
    }
    
    response = requests.post(provider.getUrl(),
        headers=headers, data=json.dumps(data)
    )
    response.raise_for_status()
    result = response.json()
    
    return result["choices"][0]["message"]["content"]

def getSystemPrompt():
    
    content = "Ты IT помощник для программистов"
    file_path = os.getenv("SYSTEM_PROMPT")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
    
    return content

def getHistoryPath():
    history_path = os.getenv("CHAT_HISTORY_PATH")
    if history_path:
        if not os.path.exists(history_path):
            os.makedirs(history_path)
        history_path = os.path.join(history_path, str(round(datetime.now().timestamp())) + ".json")
    
    return history_path

history_path = getHistoryPath()
provider = OpenRouter(os.getenv("OPENROUTER_MODEL_NAME"))

context = Context()
context.add(TextMessage(TextMessage.ROLE_SYSTEM, getSystemPrompt()))

while True:

    print ("> ", end="")
    query = input().strip()
    
    if query == "":
        continue
    if query == "q" or query == "quit":
        break
    
    context.add(TextMessage(TextMessage.ROLE_USER, query))
    response = send_llm(provider, context)
    context.add(TextMessage(TextMessage.ROLE_AI, response))
    print(response)
    
    if history_path:
        data = json.dumps(context.getData(), ensure_ascii=False)
        with open(history_path, "w") as f:
            f.write(data)
    