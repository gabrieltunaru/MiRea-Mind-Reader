import json


def get_knowledge_base():
    questions = []
    conclusions = []
    with open('questions.json', 'r') as q_file, open('conclusions.json', 'r') as c_file:
        questions = json.load(q_file)
        conclusions = json.load(c_file)
    q2 = {x['flag']: {'text': x['text'], 'required': x['required']}
          for x in questions}
    for c in conclusions:
        c['flags'] = set(c['flags'])
    return conclusions, q2


def can_ask_this_question(required_flags, flags):
    for required_flag in required_flags:
        if required_flag not in flags:
            return False
    return True


def ask(conclusions, questions):
    partial_conclusion = conclusions
    remaining_questions = questions
    flags = []
    for flag in remaining_questions:
        if not can_ask_this_question(remaining_questions[flag]['required'], flags):
            continue
        res = input(remaining_questions[flag]['text'] + " ")
        include = res == 'y'
        flags += [flag] if include else []
        partial_conclusion = list(filter(lambda x: not (
            (flag in x['flags']) ^ include), partial_conclusion))
        remaining_conclusions = len(partial_conclusion)
        if remaining_conclusions == 0:
            return "Not found"
        elif remaining_conclusions == 1:
            return partial_conclusion[0]['name']


def start():
    conclusions, questions = get_knowledge_base()
    res = ask(conclusions, questions)
    print("res:" + res)


if __name__ == '__main__':
    start()
