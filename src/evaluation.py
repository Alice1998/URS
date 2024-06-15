import pandas as pd
from openai import OpenAI

from http import HTTPStatus
import dashscope
import httpx

from zhipuai import ZhipuAI
from time import sleep


import argparse
def getParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='deepseek-chat', help='model name')
    parser.add_argument('--field', type=str, default='all', help='intent field')
    parser.add_argument('--use_saved', type=int, default=0, help='use saved file or not')
    parser.add_argument('--evaluation_model', type=str, default='gpt-4-turbo', help='evaluation model')
    parser.add_argument('--ans_model',type=str, default='gpt-4')
    args = parser.parse_args()
    return args

intent_criteria={'Factual_QA':['Factuality','User Satisfaction','Clarity','Completeness','Logical Coherence'],\
                'Solve_Professional_Problem':['Factuality','User Satisfaction','Clarity','Logical Coherence','Completeness'],\
                'Text_Assistant':['Clarity','User Satisfaction','Logical Coherence','Factuality','Creativity'],\
                'Ask_for_Advice':['User Satisfaction','Factuality','Fairness and Responsibility','Creativity','Richness'],\
                'Seek_Creativity':['User Satisfaction','Logical Coherence','Creativity','Richness','Factuality'],\
                'Leisure':['User Satisfaction','Engagement','Appropriateness','Creativity','Factuality']}

criteria={
    'Factuality': '''事实正确性(Factuality)
    提供的信息是否准确无误，是否基于可信的事实和数据''',\
    'User Satisfaction':'''满足用户需求(User Satisfaction)
    是否满足了用户提出问题的目的和需求，是否对问题进行了全面而恰当的回应''',\
    'Clarity':'''清晰度 (Clarity)
    回答是否表达清晰易懂，是否使用了简洁的语言和结构，以便用户可以轻松理解''',\
    'Completeness':'''完备性 (Completeness)
    回答是否提供了足够的信息和细节，以满足用户的需求，是否遗漏了重要的方面''',\
    'Logical Coherence':'''逻辑连贯性(Logical Coherence)
    回答是否在整体上保持一致，是否在不同部分之间保持逻辑连贯性，避免了自相矛盾''',\
    'Creativity':'''创造性(Creativity)
    是否具有创新性或独特性，是否提供了新颖，有文采的内容''',\
    'Engagement':'''趣味性 (Engagement)
    回答是否有趣、吸引人，帮助用户放松，提供了高质量的情绪价值或娱乐价值等''',\
    'Appropriateness':'''适宜性 (Appropriateness)
    内容适宜所有用户，避免不当或冒犯性内容''',\
    'Fairness and Responsibility':'''公平与可负责程度(Fairness and Responsibility)
    回答中提供的建议或信息是否可行，是否负有一定的责任，是否考虑了潜在风险和后果''',\
    'Richness':'''丰富度(Richness)
    是否包含丰富的信息、深度、上下文考虑、多样性、详细解释和实例，以满足用户需求并提供全面理解'''
}


def getInstruction(field,input_question,gpt4_answer,test_answer):
    criteria_list=intent_criteria[field]
    prompt_template=f'''请你以公正的评判者的身份，评估一个AI助手对于用户提问的回答的质量。由于您评估的回答类型是[{field}]，因此你需要从下面的5个维度对回答进行评估:
1 {criteria[criteria_list[0]]}
2 {criteria[criteria_list[1]]}
3 {criteria[criteria_list[2]]}
4 {criteria[criteria_list[3]]}
5 {criteria[criteria_list[4]]}
注意，不要让回答的长度影响你的打分！回答不是越长越好，简洁并且满足上述要求的回答是好的。

我们会给您提供用户的提问，高质量的参考答案，和需要你评估的AI助手的答案。当你开始你的评估时，你需要按照遵守以下的流程：
1. 将AI助手的答案与参考答案进行比较，指出AI助手的答案有哪些不足，并进一步解释。
2. 从不同维度对AI助手的答案进行评价，在每个维度的评价之后，给每一个维度一个1～10的分数。
3. 最后，综合每个维度的评估，对AI助手的回答给出一个1～10的综合分数。
4. 你的打分需要尽可能严格，并且要遵守下面的评分规则：总的来说，模型回答的质量越高，则分数越高。
其中，事实正确性和满足用户需求这两个维度是最重要的，这两个维度的分数主导了最后的综合分数。

当模型回答存在与问题不相关，或者有本质性的事实错误，或生成了有害内容时，总分必须是1到2分；
当模型回答没有严重错误而且基本无害，但是质量较低，没有满足用户需求，总分为3到4分；
当模型回答基本满足用户要求，但是在部分维度上表现较差，质量中等，总分可以得5到6分；
当模型回答质量与参考答案相近，在所有维度上表现良好，总分得7到8分；
只有当模型回答质量显著超过参考答案，充分地解决了用户问题和所有需求，并且在所有维度上都接近满分的情况下，才能得9到10分。
作为示例，参考答案可以得到8分。

请记住，你必须在你打分前进行评价和解释。在你对每个维度的解释之后，需要加上对该维度的打分。之后，在你回答的末尾，按照以下字典格式（包括括号）返回你所有的打分结果，并确保你的打分结果是整数： 
{{’维度一’: 打分, ’维度二’: 打分, ..., ’综合得分’: 打分}}，例如：{{'{criteria_list[0]}': 6, '{criteria_list[1]}': 8..., 'Overall': 7}}。

用户的提问：
{input_question}

[参考答案开始]
{gpt4_answer}
[参考答案结束]

[助手的答案开始]
{test_answer}
[助手的答案结束]
'''
    prompt=prompt_template
    # print(prompt)
    return prompt

def getEvaluation(evaluation_model,INPUT_TEXT):
    try:
        query_messages = [#{'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content':INPUT_TEXT}]
        if evaluation_model=='glm':
            client=ZhipuAI(api_key="") # 填写您自己的APIKey
            response = client.chat.completions.create(
                model='glm-4', # 填写需要调用的模型名称
                messages=query_messages,
            )
            x=response.choices[0].message.content
            
        elif evaluation_model=='qwen':
            dashscope.api_key = ""
            query_messages = [#{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content':INPUT_TEXT}]
            response = dashscope.Generation.call("qwen-max",
                            messages=query_messages,
                            seed=1234,
                            result_format='message')
            if response.status_code == HTTPStatus.OK:
                x=response['output']['choices'][0]['message']['content']
            else:
                x='Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                )
                raise Exception(x)
            
        elif evaluation_model=='claude':
            client = OpenAI(
                base_url="", 
                api_key="",
                http_client=httpx.Client(
                    follow_redirects=True,
                ),
            )
            completion = client.chat.completions.create(
                # model="gpt-3.5-turbo",
                # model='gpt-4-1106-preview',
                # model='gpt-4-0125-preview',
                model='claude-3-opus-20240229',
            messages=query_messages
            )
            x=completion.choices[0].message.content
        else:

            client = OpenAI(api_key="")
            completion = client.chat.completions.create(
                model=evaluation_model,
            messages=query_messages
            )
            x=completion.choices[0].message.content
    except Exception as e:
            x="Error!!!!!!\n"+str(e)
            print(x)
            sleep(5)
    return x

def main():
    args=getParser()

    field=args.field # seekCreativity
    test_model=args.model 
    df=pd.read_csv(f"../data/modelOutput_LLM={test_model}_field={field}.csv")

    # 	Unnamed: 0	question	reference_ans	user_intent	language	qwen2-72b-instruct
    reference_ans_tag='reference_ans'
    question_tag='question'
    user_intent_tag='user_intent'

    if 'evaluation' not in df.columns.tolist():
        df['evaluation']=""
    else:
        df.fillna('',inplace=True)
    for index,row in df.iterrows():
        user_intent=row[user_intent_tag]
        question=row[question_tag]
        if row[question_tag]=='' or row['evaluation']!='':
            continue

        INPUT_TEXT=getInstruction(user_intent,question,row[reference_ans_tag],row[test_model])
        result=getEvaluation(args.evaluation_model,INPUT_TEXT)
        df.loc[index,'evaluation']=result

        print(result)
        print('****** ******')
        if index%10==0:
            df[[question_tag,user_intent_tag,test_model,'evaluation']].to_csv(f'../data/evaluation_field={field}_Test={test_model}_Eval={args.evaluation_model}_Ref={reference_ans_tag}_evaluation_tmp.csv',encoding='utf-8-sig')

    df[[question_tag,user_intent_tag,test_model,test_model,'evaluation']].to_csv(f'../data/evaluation_field={field}_Test={test_model}_Eval={args.evaluation_model}_Ref={reference_ans_tag}_evaluation.csv',encoding='utf-8-sig')

if __name__ == "__main__":
    main()