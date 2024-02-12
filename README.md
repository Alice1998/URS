# User Centric Evaluation of LLMs

📍Github: [https://github.com/Alice1998/URS](https://github.com/Alice1998/URS)

📚 Blog: [User Centric Evaluation Benchmark](https://scarlet-dolomite-cc0.notion.site/User-Centric-Evaluation-of-LLMs-e2fae792b39e43ec81b5428437688720?pvs=74)

🚧 Currently Call for Contributions: [ENG](Contribution.md) | [中文](Contribution-CN.md)

💡  Share Your Experience Here  💡

[English Version](https://www.wjx.cn/vm/Qc5XIm2.aspx#) | [中文版](https://www.wjx.cn/vm/YKqvOL9.aspx# )

💡  Share Your Experience Here  💡




## Our Highlights

* **User Centric** 🏄🏻‍♀️🏄🏼🏄🏽‍♂️
  * Questions are collected through a User Survey with 411 participants
  * Different from standard evaluations and professional exams
* **Intent divided** 🙇🧑‍💻🧑‍🎨🪂
  * Objective
    * Information Retrieval, Solve Problem in Specialized Areas, (Text Assistant), Use through APIs
  * Subjective
    * Seek Creativity, Ask for Advice, Leisure

## Results

| Intents            | Solve Problem | SolveProblem GPT | Information Retrieval | API  | Ask for Advice | Seek Creativity | Leisure | All  |
| ------------------ | ------------- | ---------------- | --------------------- | ---- | -------------- | --------------- | ------- | ---- |
| #Cases             | 60            | 212              | 147                   | 26   | 58             | 57              | 60      | 620  |
| gpt-4-0125-preview | 8.58          | 7.99             | 8.34                  | 8.38 | 7.83           | 7.56            | 7.70    | 8.06 |
| ERNIE-Bot-4        | 7.68          | 7.25             | 6.93                  | 8.00 | 7.28           | 7.07            | 6.97    | 7.21 |
| qwen-max           | 7.43          | 7.28             | 7.15                  | 7.65 | 7.02           | 6.79            | 6.63    | 7.15 |
| glm-4              | 7.35          | 7.34             | 6.75                  | 8.04 | 7.17           | 6.84            | 5.95    | 7.03 |
| spark-3.5          | 6.87          | 6.77             | 6.46                  | 7.08 | 6.97           | 6.39            | 6.17    | 6.64 |
| Baichuan2-Turbo    | 6.36          | 6.61             | 6.39                  | 7.19 | 6.26           | 5.81            | 5.68    | 6.36 |
| gpt-3.5-turbo      | 6.33          | 6.55             | 6.36                  | 6.73 | 6.19           | 5.14            | 5.52    | 6.23 |
| deepseek-chat      | 6.12          | 6.92             | 5.55                  | 6.58 | 5.43           | 5.89            | 4.23    | 6.01 |

## User Intents

Description, Question Cases and Evaluation Criteria under different Intents.

| Intent                | Description                                                  | Cases                                                        | Evaluation Criteria                                          |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Solve Problem         | Seek answers or explanations in the field of programming, natural sciences, humanities, social sciences, etc.<br />Address and learn about the profession | 大模型现在为什么都是decoder-only架构<br />纯流体的粘度测试怎么做<br />烟草花叶病毒属外壳蛋白进入叶绿体的已知机制介绍<br />如何证明费马大定理？ | 1 事实正确性(Factuality),<br />2 满足用户需求(User Satisfaction), <br />3 清晰度(Clarity), <br />4 逻辑连贯性(Logical Coherence), <br />5 完备性(Completeness) |
| Information Retrieval | Fast and direct access to factual information                | 大雪农历初几<br />一加仑是多少升<br />西瓜书的目录是什么     | 1 事实正确性(Factuality),<br />2 满足用户需求(User Satisfaction), <br />3 清晰度 (Clarity), <br />4 完备性 (Completeness), <br />5 逻辑连贯性(Logical Coherence) |
| Use through APIs      | Use through Application Programming Interface instead of user interfaces<br />Explore and test the capabilities of LLM, such as evaluating it on various tasks, simulating agents, environments, or datasets, etc. | 大模型CEval评测<br />MBTI测试<br />评价模型生成内容的helpfulness | 1 事实正确性(Factuality),<br />2 满足用户需求(User Satisfaction), <br />3 清晰度(Clarity), <br />4 逻辑连贯性(Logical Coherence), <br />5 完备性(Completeness) |
| Ask for Advice        | Career development, personal counseling, gift recommendation, etc., or creating personal schedules, travel plans, shopping lists, etc. | 如何快速提高英语听力能力？<br />哪些有效方式可以缓解失眠症状？<br />适合中老年人的健康监测智能设备推荐 | 1 满足用户需求(User Satisfaction),<br />2 事实正确性(Factuality), <br />3 公平与可负责程度(Fairness and Responsibility), <br />4 创造性(Creativity), <br />5 丰富度(Richness) |
| Seek Creativity       | Brainstorming for inspiration, innovative ideas, etc.        | 设计三个生鲜超市slogan<br />我在构思经济学的课题，关于后疫情时代消费者行为变化，给我几个具体的idea<br />如何发财 | 1 满足用户需求(User Satisfaction),<br />2 逻辑连贯性(Logical Coherence), <br />3 创造性(Creativity), <br />4 丰富度(Richness), <br />5 事实正确性(Factuality) |
| Leisure               | Movie and music recommendations, games, and other entertaining activities | 下饭剧推荐<br />分享一个关于程序员的幽默笑话<br />推荐几款好玩的音乐节奏游戏 | 1 满足用户需求(User Satisfaction),<br />2 趣味性 (Engagement), <br />3 适宜性 (Appropriateness), <br />4 创造性 (Creativity), <br />5 事实正确性 (Factuality) |



## Citation

- Please cite our [Report](https://scarlet-dolomite-cc0.notion.site/User-Centric-Evaluation-of-LLMs-e2fae792b39e43ec81b5428437688720?pvs=74) if you find our work valuable, thank you!

```
@inproceedings{URS,
	title={URS: Evaluating Large Language Models on User Reported Scenarios},
	booktitle={THUIR Blog},
	year={2024}
}
```
