import json
import PySimpleGUI as sg


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
    layout = [[sg.Text("Press START to start", key='question', size=(50, 2))], [
        sg.Button("YES"), sg.Button("NO")], [sg.Text("Result", key='result', size=(50, 2))]]
    window = sg.Window(title="MiRea", layout=layout,
                       margins=(100, 100), finalize=True)
    partial_conclusion = conclusions
    remaining_questions = dict()
    current_flags = flags
    while len(partial_conclusion) > 0:
        for flag in questions:
            if not can_ask_this_question(questions[flag]['required'], flags):
                remaining_questions[flag] = questions[flag]
                continue
            window['question'].update(questions[flag]['text'])
            event, _ = window.read()
            include = event == 'YES'
            current_flags.add(flag) if include else current_flags
            partial_conclusion = list(filter(lambda x: not (
                (flag in x['flags']) ^ include), partial_conclusion))
            pcl = len(partial_conclusion)
            result = partial_conclusion[0]['name'] if pcl == 1 else "Not found"
            if pcl <= 1:
                window['result'].update(result)
                event, _ = window.Read()
                while not event == sg.WIN_CLOSED:
                    event, _ = window.Read()
                window.Close()
                return


def start():
    conclusions, questions = get_knowledge_base()
    res = ask(conclusions, questions, set())


if __name__ == '__main__':
    start()
