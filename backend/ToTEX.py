import json
q = json.loads("{\"questionName\":\"Test Question\",\"questionText\":\"How many planets are there in the solar system?\",\"answers\":[{\"answerText\":\"8\",\"correct\":true},{\"answerText\":\"3\",\"correct\":false}],\"meta\":{\"anySelectedAreCorrect\":false},\"points\":1}")
t = open('question.tex', 'w')
t.write('\\begin{question}{01-a}\n')
t.write('\t' + q['questionText'] + '\n')
t.write('\t\\begin{choices}\n')
for a in q['answers']:
	if a['correct']:
		t.write('\t\t\\correctchoice{' + a['answerText'] + '}\n')
	else:
		
		t.write('\t\t\\wrongchoice{' + a['answerText'] + '}\n')
t.write('\t\\end{choices}\n')
t.write('\\end{question}\n')
