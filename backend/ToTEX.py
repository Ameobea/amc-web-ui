''' Contains utilities for converting the intermediate JSON representation into
TeX content. '''

import datetime
from typing import List

header = '''
\\documentclass[a4paper]{article}

\\usepackage[utf8x]{inputenc}
\\usepackage[T1]{fontenc}

\\usepackage[box,completemulti]{automultiplechoice}

\\begin{document}

% Make our tests deterministically generated
% \\AMCrandomseed{1237893}

%%% Set groups to be shuffled
\\setdefaultgroupmode{withoutreplacement}

\\onecopy{10}{

%%% beginning of the test sheet header:

\\noindent{\\bf QCM  \\hfill TEST}

\\vspace
*{.5cm}

\\begin{minipage}{.4\\linewidth}

\\centering\\large\\bf Test\\\\ Examination on TODAY\\end{minipage}
\\namefield{\\fbox{
                \\begin{minipage}{.5\\linewidth}
                  Firstname and lastname:

                  \\vspace*{.5cm}\\dotfill
                  \\vspace*{1mm}
                \\end{minipage}
          }}

\\begin{center}\\em
Duration : 10 minutes.

  No notes allowed. The use of electronic calculators is forbidden.

  Questions using the sign \\multiSymbole{} may have
  zero, one or several correct answers.  Other questions have a single correct answer.
\\end{center}
\\vspace{1ex}

%%% end of the header
'''

question_body = '''
\\element{{{}}}{{
  \\begin{{question}}{{{}-a}}
    {}
    \\begin{{choices}}
{}
    \\end{{choices}}
  \\end{{question}}
}}
'''

trailer = '''
}

\\end{document}
'''

def create_answer(text: str, is_correct: bool):
    return '      \\{}{{{}}}'.format('correctchoice' if is_correct else 'wrongchoice',
                                     text)

def parse_question_dict(q: dict, index: int=1) -> str:
    answers = '\n'.join(map(lambda a: create_answer(a['answerText'], a['correct']), q['answers']))
    return question_body.format(q.get('topic') or 'default', index, q['questionText'], answers)

def parse_question_dict_list(l: List[dict]) -> str:
    output = ""
    for (i, question) in enumerate(l):
        output += parse_question_dict(question, i)
        output += "\n"
    return header + output + trailer
