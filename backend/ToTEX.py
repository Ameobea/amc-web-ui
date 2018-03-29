""" Contains utilities for converting the intermediate JSON representation into
TeX content. """

header = """
\\documentclass[a4paper]{article}

\\usepackage[utf8x]{inputenc}
\\usepackage[T1]{fontenc}

\\usepackage[box,completemulti]{automultiplechoice}

\\begin{document}

\\onecopy{10}{

%%% beginning of the test sheet header:

\\noindent{\\bf QCM  \\hfill TEST}

\\vspace
*{.5cm}

\\begin{minipage}{.4\\linewidth}

\\centering\\large\\bf Test\\\\ Examination on Jan., 1st, 2008\\end{minipage}
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
"""

trailer = """
}

\\end{document}
"""

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

    return header + output + trailer
