from openai import OpenAI
import json

class GPTChat:
    def __init__(self, prompt : str, model : str):
        self.prompt = prompt
        self.model = model
        self.client = OpenAI(
            api_key='sk-fMXML32n9lMOGmSW472f11B526E64079A6349cD44d820112',
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
# res = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     response_format={ "type": "json_object" },
#     messages=[
#         {"role": "system", "content": "你是一个电商平台的智能客服答疑助手，你会收到JSON格式的消息，内容包括客户的疑问，以及三个可能的回答选项。你的输出是JSON格式，包含三个属性：三个选项当中最合适的回答most_prob_ans，但需要与用户的问题相关；自拟一个合理回答gen_ans；以及对于你做出这个选择的原因reason"},
#         {"role": "user", "content": '''{
#          question: "我该如何修改我的账户密码？",
#          ans_1: "我们接受信用卡、",
#          ans_2: "如果您在订购时遇到了付款问题，请尝试使用其他付款方式，例如信用卡、借记卡、PayPal等。如果仍然无法解决问题，请联系我们的客户服务部门以获取更多帮助。",
#          ans_3: "您好，请先确认您输入的支付信息是否正确。如果还是无法支付，请您联系银行或支付平台进行咨询。如果问题依然存在，您也可以联系我们的客服人员协助您解决。",
#         }'''},
#     ], 
# )
# gpt = GPTChat("你是一个电商平台的智能客服答疑助手，你会收到JSON格式的消息，内容包括客户的疑问，以及三个可能的回答选项。你的输出是JSON格式，包含两个属性：三个选项当中最合适的回答most_prob_ans，但需要与用户的问题相关，若不相关或未回答该问题，则用null填充本属性；自拟一个合理回答gen_ans")
# gpt = GPTChat("你是一个电商平台的智能客服答疑助手，你会收到JSON格式的消息，内容包括客户的疑问question，以及三个可能的回答选项ans_1-3。你的输出是JSON格式，包含属性：自拟一个合理回答gen_ans")

# res = gpt.getGPTResponse({
#     "question": "你们支持哪些支付方式？",
#     "ans_1": "我们接受信用卡、",
#     "ans_2": "如果您在订购时遇到了付款问题，请尝试使用其他付款方式，例如信用卡、借记卡、PayPal等。如果仍然无法解决问题，请联系我们的客户服务部门以获取更多帮助。",
#     "ans_3": "您好，请先确认您输入的支付信息是否正确。如果还是无法支付，请您联系银行或支付平台进行咨询。如果问题依然存在，您也可以联系我们的客服人员协助您解决。",
# })
# print(res)

# gpt = GPTChat("""
#               你是一个电商平台客服，你会收到JSON格式的消息，消息格式为：
#               {
#               'question' : '用户的问题',
#               'orders' : 
#                 [
#                     {
#                         'order_id' : '订单号',
#                         'product' : '产品名称',
#                         'price' : '价格',
#                         'status' : '状态',
#                     }, 
#                     ...
#                 ]
#               }
#               你需要根据用户的问题，必要时可以参考用户的订单信息，回答用户的问题，回答尽量简洁一些。
#               你需要输出JSON格式的消息，为：
#               {'gen_ans' : '你的回答'}
#               """)
# orders = [{'order_id': '123456', 'product': '手机', 'price': '1999', 'status': '已发货'}, 
#           {'order_id': '123457', 'product': '电脑', 'price': '5999', 'status': '已签收'}]
# question = "订单号123456是什么货物？"
# res = None
# for _ in range(3):
#     try:
#         res = gpt.getGPTSeveralResponses({
#             'question': question,
#             'orders': orders
#         })
#         print(res)
#         break
#     except:
#         print("retrying...")
# for _ in range(3):
#     try:
#         res = gpt.getGPTSeveralResponses({
#             'question': "这个货物的价格是多少？",
#             'orders': orders
#         })
#         print(res)
#         break
#     except:
#         print("retrying...")

