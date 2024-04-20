field_list=('Factual_QA' 'Solve_Professional_Problem'  'API' 'Text_Assistant' 'Seek_Creativity' 'Ask_for_Advice' 'Leisure')
model='ERNIE-Bot-4'

task() {
    field=$1
    echo "[${field}] start!"
    python getModelOutput.py --model "${model}" --field "${field}"
    echo "[${field}] finish get ans"
    echo "[${field}] start evaluation"
    python evaluation.py --model "${model}" --field "${field}"
    echo "[${field}] finish evaluation"
}

# 并行执行任务1到5
task "${field_list[0]}" &
task "${field_list[1]}" &
task "${field_list[2]}" &
task "${field_list[3]}" &
task "${field_list[4]}" &
task "${field_list[5]}" &
