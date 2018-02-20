import json

def parse_dict(q: dict) -> str:
    output = ""

    output += '\\begin{question}{01-a}\n'
    output += '\t' + q['questionText'] + '\n'
    output += '\t\\begin{choices}\n'
    for a in q['answers']:
        if a['correct']:
            output += '\t\t\\correctchoice{' + a['answerText'] + '}\n'
        else:

            output += '\t\t\\wrongchoice{' + a['answerText'] + '}\n'
    output += '\t\\end{choices}\n'
    output += '\\end{question}\n'

    return output
