''' Contains utilities for converting the intermediate JSON representation into
TeX content. '''

import datetime
from typing import List

header1 = '''
\\documentclass[a4paper]{article}

\\usepackage[utf8x]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[box,completemulti,separateanswersheet]{automultiplechoice}

\\begin{document}

% Make our tests deterministically generated
\\AMCrandomseed{1237893}

\\def\\AMCformQuestion#1{\\vspace{\\AMCformVSpace}\\par {\\sc Question #1:} }

%%% Set groups to be shuffled
% \\setdefaultgroupmode{withoutreplacement}
'''

header2 = '''
\\onecopy{COPIES}{

%%% beginning of the test sheet header:

\\noindent{\\bf QCM  \\hfill TEST}

\\vspace*{.5cm}
\\begin{minipage}{.4\\linewidth}
  \\centering\\large\\bf Test\\ Examination on TODAY'S DATE
\\end{minipage}

\\begin{center}\\em
Duration : 10 minutes.

  No notes allowed. The use of electronic calculators is forbidden.

  Questions using the sign \\multiSymbole{} may have
  zero, one or several correct answers.  Other questions have a single correct answer.
\\end{center}
\\vspace{1ex}

%%% end of the header
'''

answersheet = '''
%%% beginning of the answer sheet header

% Insert a double page break
\\clearpage

\\AMCformBegin

{\\large\\bf Answer sheet:}
\\hfill \\namefield{\\fbox{
     \\begin{minipage}{.5\\linewidth}
        Firstname and lastname:

        \\vspace*{.5cm}\\dotfill
        \\vspace*{1mm}
    \\end{minipage}
  }}

\\begin{center}
  \\bf\\em Answers must be given exclusively on this sheet:
  answers given on other sheets will be ignored.
\\end{center}

%%% end of the answer sheet header

\\AMCform
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

def parse_question_dict_list(l: List[dict], copies=10) -> str:
    output = ''
    for (i, question) in enumerate(l):
        output += parse_question_dict(question, i)
        output += '\n'

    groups = ''
    topics = set(map(lambda q: q.get('topic') or 'default', l))
    for topic in topics:
        groups += '\\insertgroup{{{}}}\n\n'.format(topic)

    our_header2 = header2.replace('COPIES', str(copies))
    return header1 + output + our_header2 + groups + answersheet + trailer
