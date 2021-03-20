import json


def get_knowledge_base():
    questions = []
    conclusions = []
    with open('questions.json', 'r') as q_file, open('conclusions.json', 'r') as c_file:
        questions = json.load(q_file)
        conclusions = json.load(c_file)
    q2 = {x['flag']: {'text': x['text'], 'required': set(x['required'])}
          for x in questions}
    for c in conclusions:
        c['flags'] = set(c['flags'])
    return conclusions, q2


def can_ask_this_question(required_flags, flags):
    return True if len(required_flags - flags) == 0 else False


def ask(conclusions, questions, flags):
    partial_conclusion = conclusions
    remaining_questions = dict()
    current_flags = flags
    for flag in questions:
        if not can_ask_this_question(questions[flag]['required'], flags):
            remaining_questions[flag] = questions[flag]
            continue
        res = input(questions[flag]['text'] + " ")
        include = res == 'y'
        current_flags.add(flag) if include else current_flags
        partial_conclusion = list(filter(lambda x: not (
            (flag in x['flags']) ^ include), partial_conclusion))
        remaining_conclusions = len(partial_conclusion)
        if remaining_conclusions == 0:
            return "Not found"
        elif remaining_conclusions == 1:
            return partial_conclusion[0]['name']
    return ask(partial_conclusion, remaining_questions, current_flags)


def start():
    conclusions, questions = get_knowledge_base()
    res = ask(conclusions, questions, set())
    print("res:" + res)


if __name__ == '__main__':
    start()
