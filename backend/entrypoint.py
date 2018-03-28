import json
import pythonWrapper
from os import path

from flask import Flask, request
from flask_cors import CORS



from ToTEX import parse_dict

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route("/example_json_post", methods=["POST"])
def process_question():
    print(request.json)

    body = request.json
    return json.dumps(body)

@app.route("/generate_tex", methods=["POST"])
def generate_tex():
    j = request.json

    return parse_dict(j)

@app.route("/create_project", methods=["POST"])
def generate_pdf():
    j = request.json

    with open('text.tex', mode='w') as quiz_file:
        quiz_file.write(parse_dict(j))
        quiz_file.close()

    project_name = 'pythonTest4'
    project_dir = pythonWrapper.createProject(project_name)
    pythonWrapper.addQuestion('text.tex', project_dir, project_name)
    pythonWrapper.prepareQuestion(project_dir, 'text.tex', 'TheNameOfThePDF')

    return project_dir

app.run(host='0.0.0.0', port=4545)
