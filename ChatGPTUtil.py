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
        self.history = []
        self.history.append({"role": "system", "content": self.prompt})

    def getGPTResponse(self, question : str) -> str:
        resp = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": question},
            ], 
        )
        return resp.choices[0].message.content
    
    def getJsonResponse(self, question : str) -> dict:
        resp = self.client.chat.completions.create(
            model = self.model,
            response_format = { "type": "json_object" },
            messages = [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": question},
            ], 
        )
        # resp_dict = json.loads(resp.choices[0].message.content)
        # return resp_dict
        return resp.choices[0].message.content
    
    def getGPTResponseAskingJson(self, question : dict) -> dict:
        resp = self.client.chat.completions.create(
            model = self.model,
            response_format = { "type": "json_object" },
            messages = [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": json.dumps(question, ensure_ascii=False)},
            ], 
        )
        return json.loads(resp.choices[0].message.content)
    
    def getGPTSeveralJsonResponses(self, question : list) -> dict:
        self.history.append({"role": "user", "content": json.dumps(question, ensure_ascii=False)})
        resp = self.client.chat.completions.create(
            model = self.model,
            response_format = { "type": "json_object" },
            messages = self.history, 
        )
        resp_dict = json.loads(resp.choices[0].message.content)
        self.history.append({"role": "system", "content": resp_dict['gen_ans']})
        return resp_dict
    
    def getGPTSeveralResponsesAskingJson(self, question : dict) -> str:
        self.history.append({"role": "user", "content": json.dumps(question, ensure_ascii=False)})
        resp = self.client.chat.completions.create(
            model = self.model,
            messages = self.history, 
        )
        self.history.append({"role": "system", "content": resp.choices[0].message.content})
        return resp.choices[0].message.content
    
    def getGPTResponseDefineHistory(self):
        pass

