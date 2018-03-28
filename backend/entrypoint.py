import json
import pythonWrapper

from flask import Flask, request
from flask_cors import CORS

from ToTEX import parse_dict

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route("/example_json_post", methods=["POST"])
def process_question():
    print(request.json)

    body = request.json
#    body['a'] = body['a'] + 1


	
    return json.dumps(body)

@app.route("/generate_tex", methods=["POST"])
def generate_tex():
    j = request.json
    
    return parse_dict(j)

@app.route("/create_project", methods=["POST"])
def generate_pdf():
    j = request.json
    quiz = open('test.tex', 'w')
    quiz.write(parse_dict(j))
    quiz.close()
    pythonWrapper.createProject('pythonTest4', pythonWrapper.getDirFromConfig()+ '/')
    pythonWrapper.addQuestion(pythonWrapper.getSampleTexFileLocation() + 'simple.tex', pythonWrapper.getDirFromConfig(), 'pythonTest4')
    pythonWrapper.prepareQuestion(pythonWrapper.getDirFromConfig()+'/'+'pythonTest4', 'simple.tex', 'TheNameOfThePDF')
#    return "Success"
    return pythonWrapper.getDirFromConfig()

app.run(host='0.0.0.0', port=4545)
