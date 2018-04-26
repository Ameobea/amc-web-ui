''' Contains utilities for converting the intermediate JSON representation into TeX content. '''

from typing import List

HEADER_1 = '''
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

HEADER_2 = '''
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

ANSWER_SHEET_SPEC = '''
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

QUESTION_BODY_SPEC = '''
\\element{{{}}}{{
  \\begin{{question}}{{{}-a}}
    {}
    \\begin{{choices}}
{}
    \\end{{choices}}
  \\end{{question}}
}}
'''

TRAILER = '''
}

\\end{document}
'''

def create_answer(text: str, is_correct: bool):
    ''' Generates the LaTeX code for a single question given its content and whether it is correct
    or not. '''

    return '      \\{}{{{}}}'.format('correctchoice' if is_correct else 'wrongchoice',
                                     text)

def parse_question_dict(questions: dict, index: int = 1) -> str:
    ''' Given a dictionary representing a question, returns the corresponding LaTeX code that
    will be injected into the generated .tex file to represent it on the quiz.  The provided
    dict should have the following structure:

    ```py
    {
        'questionText': 'Which is the closest plane to the sun in the solar system?',
        'answers': [
            {
                'answerText': 'Saturn',
                'isCorrect': False,
            },
            {
                'answerText': 'Mercury',
                'isCorrect': True,
            }
        ],
        'topic': 'Astronomy', // Optional; defaults to "default"
    }
    ```
    '''

    answers = '\n'.join(map(
        lambda a: create_answer(a['answerText'], a['correct']), questions['answers']))

    return QUESTION_BODY_SPEC.format(
        questions.get('topic') or 'default',
        index,
        questions['questionText'],
        answers)

def parse_question_dict_list(question_list: List[dict], copies: int = 10) -> str:
    ''' Given a list of questions in the schema detailed in the `parse_question_dict` function,
    parses them all into LaTeX, combines them with the header and trailer required to produce
    a valid AMC .tex file, and returns the generated LaTeX source code as a string. '''

    output = ''
    for (i, question) in enumerate(question_list):
        output += parse_question_dict(question, i)
        output += '\n'

    groups = ''
    topics = set(map(lambda q: q.get('topic') or 'default', question_list))
    for topic in topics:
        groups += '\\insertgroup{{{}}}\n\n'.format(topic)

    our_header2 = HEADER_2.replace('COPIES', str(copies))
    return HEADER_1 + output + our_header2 + groups + ANSWER_SHEET_SPEC + TRAILER
