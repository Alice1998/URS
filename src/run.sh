# model_list=['glm-4','gpt-3.5-turbo','deepseek-chat','spark-3.5','Baichuan2-Turbo','qwen-max','gpt-4-0125-preview','ERNIE-Bot-4']
# 'gpt-4-0125-preview','ERNIE-Bot-4'

python evaluation.py --model ERNIE-Bot-4 --field SolveProblemGPT &
python evaluation.py --model qwen-max --field SolveProblemGPT &

python evaluation.py --model glm-4 --field SolveProblemGPT &
python evaluation.py --model spark-3.5 --field SolveProblemGPT &

python evaluation.py --model Baichuan2-Turbo --field SolveProblemGPT &
python evaluation.py --model deepseek-chat --field SolveProblemGPT &

python evaluation.py --model gpt-4-0125-preview --field SolveProblemGPT &
python evaluation.py --model gpt-3.5-turbo --field SolveProblemGPT &