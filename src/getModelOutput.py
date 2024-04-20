import pandas as pd
from openai import OpenAI
from zhipuai import ZhipuAI


class APIclass():
    def __init__(self,model_name):
        self.model_name=model_name
        return
    
    def get_response(self, INPUT_TEXT):
        pass


class OpenAIFormat(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        if model_name=='deepseek-chat':
            self.client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")
        else:
            self.client = OpenAI()
            

    def get_response(self, INPUT_TEXT):
        response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": INPUT_TEXT},
                ]
            )
        answer=response.choices[0].message.content
        print(answer)
        print("****** ******")
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
        print(answer)
        print("****** ******")
        return answer


import requests
import json


class Baichuan():
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
        print(answer)
        print("****** ******")
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
        if self.model_name=='qwen-turbo':
            response = dashscope.Generation.call(
                dashscope.Generation.Models.qwen_turbo, #qwen_max_1201,#qwen_turbo,
                messages=messages,
                result_format='message',  # set the result to be "message" format.
            )
        elif self.model_name=='qwen-max':
            response = dashscope.Generation.call(
                dashscope.Generation.Models.qwen_max, #qwen_max_1201,#qwen_turbo,
                messages=messages,
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
        print(ans)
        print("****** ******")
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
        print(ans)
        print("****** ******")
        return ans

from APIs import SparkApi
class Spark(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        
        self.appid = ""     #填写控制台中获取的 APPID 信息
        self.api_secret = ""   #填写控制台中获取的 APISecret 信息
        self.api_key =""
        
        if model_name=='spark-3.5':
            self.domain='generalv3.5'
            self.Spark_url="ws://spark-api.xf-yun.com/v3.5/chat"
    
    def getText(self,role,content):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        return [jsoncon]
    
    def get_response(self, INPUT_TEXT):
        question = self.getText("user", INPUT_TEXT)
        SparkApi.answer = ""
        SparkApi.main(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, question)
        ans=SparkApi.answer
        return ans
    
import anthropic
class Anthropic(APIclass):
    def __init__(self,model_name):
        self.model_name=model_name
        self.client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=""
        )

    
    def get_response(self, INPUT_TEXT):
        # response = self.client.chat.completions.create(
        #         model=self.model_name,
        #         messages=[
        #             # {"role": "system", "content": "You are a helpful assistant"},
        #             {"role": "user", "content": INPUT_TEXT},
        #         ],
        #     )
        # ans=response.choices[0].message.content


        message = self.client.messages.create(
            model=self.model_name, #"claude-3-opus-20240229",
            # system="Respond only in Yoda-speak.",
            messages=[
                {"role": "user", "content": INPUT_TEXT}
            ]
        )
        ans=message.content[0].text
        if 'Error code:' in ans:
            print(ans)
            raise Exception(ans)
        return ans


def getModelClass(model_name): # tag -> INPUT_TEXT
    if model_name=='deepseek-chat' or model_name=='gpt-3.5-turbo' or model_name=="gpt-4-0125-preview":
        return OpenAIFormat(model_name)
    elif model_name=='claude-3-opus-20240229':
        return Anthropic(model_name)
    elif model_name=='glm-4':
        return ZhiPu(model_name)
    elif model_name=='Baichuan2-Turbo':
        return Baichuan(model_name)
    elif model_name=='qwen-turbo' or model_name=='qwen-max':
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


def getOutput(model_name,tag):
    try:
        model= getModelClass(model_name)
    except Exception as e:
        print(e)
        return df_question
    if model_name not in df_question.columns.tolist():
        df_question[model_name]=""
    df_question.fillna("",inplace=True)

    for index,row in df_question.iterrows():
        INPUT_TEXT = row[tag]
        if INPUT_TEXT=='' or INPUT_TEXT=="无" or row[model_name]!='':
            # print(INPUT_TEXT,row[model_name])
            continue
        try:
            answer=model.get_response(INPUT_TEXT)
        except Exception as e:
            answer="Error!!!!!!\n"+str(e)
            print(answer)
            print("****** ******")
            return df_question
        print(answer)
        print("****** ******")
        df_question.loc[index,model_name]=answer
        if index%10==0:
            df_question[[tag,model_name]].to_csv(f"../data/modelOutput/{field}_{model_name}_tmp.csv",encoding='utf-8-sig')
    return df_question


model_list=['deepseek-chat','gpt-3.5-turbo','gpt-4-0125-preview','glm-4',"Baichuan2-Turbo",'qwen-turbo','qwen-max',"ERNIE-Bot-4"]


import argparse
def getParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='deepseek-chat', help='model name')
    parser.add_argument('--field', type=str, default='Factual QA', help='intent')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args=getParser()

    file_path="../data/data_all.csv"

    test_model=args.model
    # test_model='gpt-4-0125-preview'
    # test_model='ERNIE-Bot-4'
    # test_model='glm-4'
    # test_model='gpt-3.5-turbo'
    # test_model='deepseek-chat'
    # test_model='Baichuan2-Turbo'
    # test_model='qwen-turbo'
    # test_model='qwen-max'

    field=args.field
     tag='question'

    df_question= pd.read_csv(file_path)
    df_question=df_question[df_question['user_intent']==field]

    print(field)
    print(len(df_question))
    print(test_model)

    df_ans=getOutput(test_model,tag)


    df_ans[[tag,test_model]].to_csv(f"../data/modelOutput/{field}_{test_model}.csv",encoding='utf-8-sig')