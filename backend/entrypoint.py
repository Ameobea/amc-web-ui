""" Defines an API that can be used to interact with Auto Multiple Choice.  Exposes this
API via a HTTP interface using the Flask webserver. """

import json
from os import path

from flask import Flask, request, send_file, url_for, render_template
from flask_cors import CORS

from ToTEX import parse_dict, parse_dict_list
import pythonWrapper

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route("/", methods=["GET"])
def serve_index():
    # return render_template(url_for('static', filename='index.html'))
    return app.send_static_file('index.html')

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

    project_name = 'pythonTest4'
    project_dir = pythonWrapper.createProject(project_name)
    tex_file_path = path.join(project_dir, 'text.tex')

    with open(tex_file_path, mode='w') as quiz_file:
        quiz_file.write(parse_dict_list(j))
        quiz_file.close()

    pythonWrapper.prepareQuestion(project_dir, tex_file_path, 'TheNameOfThePDF')

    pdf_path = path.join(project_dir, 'DOC-subject.pdf')
    return send_file(pdf_path, attachment_filename='generated_quiz.pdf')

    return project_dir

app.run(host='0.0.0.0', port=4545)
