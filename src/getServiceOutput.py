import pandas as pd
from openai import OpenAI
from zhipuai import ZhipuAI
from time import sleep


class APIclass():
    def __init__(self,model_name):
        self.model_name=model_name
        return
    
    def get_response(self, INPUT_TEXT):
        pass

import httpx

class OpenAIFormat(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        if model_name=='deepseek-chat':
            self.client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")
        else:
            self.client = OpenAI(api_key="")


            
    def get_response(self, INPUT_TEXT):
        response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": INPUT_TEXT},
                ]
            )
        answer=response.choices[0].message.content
        return answer


class Moonshot(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        self.client=OpenAI(
            api_key="",
            base_url="https://api.moonshot.cn/v1")
        
    def get_response(self, INPUT_TEXT):
        response = self.client.chat.completions.create(
                model=self.model_name, # moonshot-v1-8k
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": INPUT_TEXT},
                ],
            )
        answer=response.choices[0].message.content
        sleep(14)
        return answer
    

class ZhiPu(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        self.client = ZhipuAI(api_key="") # 填写您自己的APIKey

    def get_response(self, INPUT_TEXT):
        response = self.client.chat.completions.create(
            model=self.model_name,  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": INPUT_TEXT}
            ],
        )
        answer=response.choices[0].message.content  
        return answer


import requests
import json


class Baichuan(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        self.url = "https://api.baichuan-ai.com/v1/chat/completions"
        self.api_key = ""
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

    def get_response(self, INPUT_TEXT):
        data = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": INPUT_TEXT
                }
            ],
            "stream": False
        }
        json_data = json.dumps(data)

        response = requests.post(self.url, data=json_data, headers=self.headers, timeout=60)
        x=eval(response.text)
        answer=x['choices'][0]['message']['content']
    
        # if response.status_code == 200:
        #     print("请求成功！")
        #     print("响应body:", response.text)
        #     print("请求成功，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
        # else:
        #     print("请求失败，状态码:", response.status_code)
        #     print("请求失败，body:", response.text)
        #     print("请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
        # answer=response.text
        # print(answer)
        # print("****** ******")
        return answer

from http import HTTPStatus
import dashscope

class Qwen(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        dashscope.api_key = ""

    def get_response(self,INPUT_TEXT):
        messages = [#{'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content':INPUT_TEXT}]
        response = dashscope.Generation.call(
            self.model_name,
            messages=messages,
            # set the random seed, optional, default to 1234 if not set
            result_format='message',  # set the result to be "message" format.
        )
        
        if response.status_code == HTTPStatus.OK:
            ans=response['output']['choices'][0]['message']['content']
            
        else:
            ans='Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            )
            raise Exception(ans)
        # print(ans)
        # print("****** ******")
        return ans

import requests
import json

class Baidu(APIclass):
    def get_access_token(self):
        """
        使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
        """
        client_id=""
        secret_key=""
            
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={secret_key}"
        
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")
    
    def __init__(self,model_name):
        self.model_name=model_name
        self.url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + self.get_access_token()
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_response(self, INPUT_TEXT):
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": INPUT_TEXT
                }
            ]
        })
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        ans_dict = json.loads(response.text)
        ans=ans_dict['result']
        # print(ans)
        # print("****** ******")
        return ans


    
import anthropic
class Anthropic(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
    

        api_key = ""
        api_base = ""
        self.client = OpenAI(api_key=api_key, base_url=api_base)

    def get_response(self, INPUT_TEXT):

        response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": INPUT_TEXT},
                ],
            )
        ans=response.choices[0].message.content


        # message = self.client.messages.create(
        #     model=self.model_name, #"claude-3-opus-20240229",
        #     max_tokens=1000,
        #     temperature=0.3,
        #     # system="Respond only in Yoda-speak.",
        #     messages=[
        #         {"role": "user", "content": INPUT_TEXT}
        #     ]
        # )
        # ans=message.content[0].text
        # if 'Error code:' in ans:
        #     print(ans)
        #     raise Exception(ans)
        return ans


from serpapi import GoogleSearch
class Google(APIclass):
    def __init__(self):
        self.API=''

    def get_response(self, INPUT_TEXT):

        params = {
        "engine": "google",
        "q": INPUT_TEXT,
        "location": "Haidian,Beijing,China",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "num": "10",
        "start": "10",
        "safe": "active",
        "api_key": self.API
        }
        search = GoogleSearch(params)
        if 'answer_box' in search:
            print(search['answer_box']['snippet'])
        for line in search['organic_results']:
            print(line['position'])
            print(line['title'])
            print(line['snippet'])
            print(line['link'])
        return search

def getModelClass(model_name): # tag -> INPUT_TEXT
    if model_name=='deepseek-chat' or model_name=='gpt-3.5-turbo' or model_name=="gpt-4-1106-preview" or model_name=="gpt-4-0125-preview" or model_name=='gpt-4' or model_name=="gpt-4-turbo" or model_name=='gpt-4o':
        return OpenAIFormat(model_name)
    elif model_name=='claude-3-opus-20240229':
        return Anthropic(model_name)
    elif model_name=='moonshot-v1-8k':
        return Moonshot(model_name)
    elif model_name=='glm-4':
        return ZhiPu(model_name)
    elif model_name=='Baichuan2-Turbo':
        return Baichuan(model_name)
    elif model_name=='qwen-turbo' or model_name=='qwen-max' or model_name=='qwen2-72b-instruct':
        return Qwen(model_name)
    elif model_name=='ERNIE-Bot-4':
        return Baidu(model_name)
    elif model_name=='spark-3.5':
        return Spark(model_name)
    else:
        ans="Incorrect model name"+model_name
        print(ans)
        raise Exception(ans)
        return APIclass()


def getOutput(df_question,model_name):
    if model_name not in df_question.columns.tolist():
        df_question[model_name]=""
    df_question.fillna("",inplace=True)

    for index,row in df_question.iterrows():
        INPUT_TEXT = row['question']
        if INPUT_TEXT=='' or INPUT_TEXT=="无" or row[model_name]!='':
            continue
        try:
            try:
                model= getModelClass(model_name)
            except Exception as e:
                print(e)
                return df_question
            answer=model.get_response(INPUT_TEXT)
        except Exception as e:
            answer="****** Error! ******\n"+str(e)
            print(answer)
            print("****** ******")
            # return df_question
        print(answer)
        print("****** ******")
        df_question.loc[index,model_name]=answer
        if index%10==0:
            df_question[['question',model_name]].to_csv(f"../data/modelOutput_{test_model}_tmp.csv",encoding='utf-8-sig')
    return df_question


model_list=['deepseek-chat','gpt-3.5-turbo','gpt-4-1106-preview','gpt-4-0125-preview','glm-4','moonshot-v1-8k',"Baichuan2-Turbo",'qwen-turbo','qwen-max',"ERNIE-Bot-4",'gpt-4','claude-3-opus-20240229','qwen2-72b-instruct','gpt-4o']


import argparse
def getParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='gpt-4o', help='model name')
    parser.add_argument('--field', type=str, default='all', help='intent field')
    parser.add_argument('--use_saved', type=int, default=0, help='load saved file or not')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args=getParser()


    field=args.field
    test_model=args.model
    df=pd.read_csv("../data/evaluation_question.csv")
    if field!='all':
        if field in ['Solve_Professional_Problem','Factual_QA','Text_Assistant','Ask_for_Advice','Seek_Creativity','Leisure']:
            df=df[df['user_intent']==field]
        else:
            print("Incorrect field name")
            # raise Exception("Incorrect field name")
    

    df_ans=getOutput(df,test_model)
    df_ans.to_csv(f"../data/modelOutput_LLM={test_model}_field={field}.csv",encoding='utf-8-sig')
