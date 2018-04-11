""" Defines an API that can be used to interact with Auto Multiple Choice.  Exposes this
API via a HTTP interface using the Flask webserver. """

import json
from os import path

from flask import Flask, jsonify, request, send_file, url_for, render_template
from flask_cors import CORS

from ToTEX import parse_dict, parse_dict_list
import pythonWrapper
from db import insert_questions, query_questions

app = Flask(__name__, static_url_path='')
CORS(app)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['success'] = False
        return rv

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

@app.route("/store_questions", methods=["POST"])
def store_questions():
    j = request.json

    if (not j.get('topic')) or (not j.get('username')):
        raise InvalidUsage("You must supply both a topic and a username!")

    if (not j.get('questions')) or not len(j['questions']):
        raise InvalidUsage("You must supply questions to store!")

    insert_questions(j['questions'], topic=j['topic'], username=j['username'])

    return jsonify({
        "success": True,
        "message": "Questions successfully stored."
    })

@app.route("/find_questions", methods=["POST"])
def find_questions():
    j = request.json
    db_res = query_questions(j.get('topic'), j.get('username'), j.get('question_text'))
    return jsonify(db_res)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(host='0.0.0.0', port=4545)
