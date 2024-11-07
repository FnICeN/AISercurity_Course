from openai import OpenAI
import json

class GPTChat:
    def __init__(self, prompt : str, model : str):
        self.prompt = prompt
        self.model = model
        self.client = OpenAI(
            api_key='sk-aoLMZiLNuDUpQQhJ181aDaB0D5E34f6b928dFf8dEc8aDa6f',
            base_url="https://api.gpt.ge/v1/",
        )
    
    def getRespWithDefinedHistory(self, definedHistory : list) -> str:
        resp = self.client.chat.completions.create(
            model = self.model,
            messages = [{"role": "system", "content": self.prompt}] + definedHistory, 
        )
        return resp.choices[0].message.content
    
    def getJsonRespWithDefinedHistory(self, definedHistory : list) -> dict:
        resp = self.client.chat.completions.create(
            model = self.model,
            messages = [{"role": "system", "content": self.prompt}] + definedHistory, 
        )
        return json.loads(resp.choices[0].message.content)