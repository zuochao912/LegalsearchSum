import requests
import json
import time
from queue import Queue

headers = {
    'Authorization': '',
    'Content-Type': 'application/json',
} # 输入对应的API;

# 关键词抽取template
template1="你是一位懂得法律知识的法律专家，现在你需要做法律文书的关键词提取任务。现在给定法律文书如下。{}你需要对上述法律文书做关键词提取，注意形成方便其他法律专家做类案检索任务的关键词，并用逗号隔开各个词语，逐个输出如下" # 方案二
template2="你是一位懂得法律知识的法律专家，现在你需要做法律文书的关键词提取任务。现在给定法律文书如下。{}你需要判断出对于法律案件判决具有重要参考价值的词语，并用逗号隔开各个词语。注意在本任务中，人名、地点、时间等词语都不是重要的词语，所以不要输出他们。" # 方案六
# 关键语句抽取template
template3="你是一位懂得法律知识的法律专家，现在你需要做法律文书的关键语句提取任务。现在给定法律文书如下。{}你需要对上述法律文书提取关键语句，注意关键语句是对最终案例裁决起到关键作用的语句。"
# 摘要抽取template
template4="你是一位懂得法律知识的法律专家，现在你需要做法律关键内容抽取任务。现在给定法律文书如下。{}你需要对上述法律文书做摘要，摘要如下："
template5="你是一位懂得法律知识的法律专家，现在你需要做法律关键内容抽取任务。现在给定法律文书如下。{}你需要对上述法律文书做摘要，注意形成方便其他法律专家做类案检索任务的摘要。摘要如下："

# revise annot;
templatex="请为下列分隔开的语句加上标点符号，使他们变为连贯的语句。{}" # 方案二

templates=[template1,template2,template3,template4,template5]
namels=["chat_word1","chat_word2","chat_sent1","chat_sum1","chat_sum2"]

results=[{} for i in range(len(templates))]

queue_obj = Queue()
q_p="query.json"
# q_p="annot_query_sent.json"
entrydict={}

with open(q_p,"r",encoding="utf-8") as fr:
    lines=fr.readlines()
    for line in lines:
        linedict=json.loads(line)
        qid=linedict["ridx"]
        queue_obj.put(qid)
        entrydict[qid]=linedict["q"]

counts=0
while not queue_obj.empty():
    qid=queue_obj.get()
    q=entrydict[qid]
    counts+=1
    # print("qid:{},length:{}".format(qid,len(q)))
    for idx,tmp in enumerate(templates):
        content=tmp.format(q)
        datadic = { 
            "model": "gpt-3.5-turbo", 
            "stream": False, 
            "temperature":0.9,
            "max_tokens":4000,
            "top_p":1,
            "frequency_penalty":0.2,
            "presence_penalty":0.2,
            "messages": [ { "role": "user", "content": "{}".format(content) } ] }
        data= json.dumps(datadic)

        try:
            time.sleep(1)
            response = requests.post('xxx', headers=headers, data=data) # 请修改为对应的api接口;
            # print(response)
            reply=json.loads(response.content.decode("utf-8"))
            choices=reply["choices"]
            # print(len(choices))
            replycont=choices[0]["message"]["content"]
            results[idx][qid]=replycont

        except:
            # print()
            print("Network error for query:{}".format(qid))
            queue_obj.put(qid)
            for i in range(len(templates)):
                tar_p="./revise/{}.json".format(namels[i])
                with open(tar_p,"w",encoding="utf-8") as fw:
                    json.dump(results[i],fw,ensure_ascii=False)

    if (counts+1) %10==0:
        print("Having processed {}".format(counts))
        for i in range(len(templates)):
            tar_p="./revise/{}.json".format(namels[i])
            with open(tar_p,"w",encoding="utf-8") as fw:
                json.dump(results[i],fw,ensure_ascii=False)

# 注意改成一行一行的...每行一个dict,是{"ridx":id,"q":q}格式的,否则lexical model训练测试读不出来
for i in range(len(templates)):
    tar_p="./revise/{}.json".format(namels[i])
    with open(tar_p,"w",encoding="utf-8") as fw:
        json.dump(results[i],fw,ensure_ascii=False)
