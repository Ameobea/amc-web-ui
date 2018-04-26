""" Defines an API that can be used to interact with Auto Multiple Choice.  Exposes this
API via a HTTP interface using the Flask webserver. """

import json
from os import path
from typing import List

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from ToTEX import parse_question_dict, parse_question_dict_list
import pythonWrapper
from db import insert_questions, query_questions, store_test, retrieve_tests

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

    return parse_question_dict(j)

def validate_json(j: dict, keys: List[str]):
    for key in keys:
        if not j.get(key):
            raise InvalidUsage('You must supply a {} param.'.format(key))

@app.route("/create_project", methods=["POST"])
def generate_pdf():
    j = request.json
    validate_json(j, ['name', 'username', 'questions'])

    # Save the test definition to the database for later usage
    store_test(j['name'], j['username'], j['questions'])

    project_dir = pythonWrapper.createProject(j['name'])
    print(project_dir)
    tex_file_path = path.join(project_dir, 'text.tex')

    with open(tex_file_path, mode='w') as quiz_file:
        quiz_file.write(parse_question_dict_list(j['questions'], copies=j.get('copies')))
        quiz_file.close()

    pythonWrapper.prepareQuestion(project_dir, tex_file_path, 'TheNameOfThePDF')

    pdf_path = path.join(project_dir, 'DOC-subject.pdf')

    # TODO: cleanup project directory
    return send_file(pdf_path, attachment_filename='generated_quiz.pdf')

@app.route("/store_questions", methods=["POST"])
def store_questions():
    j = request.json
    validate_json(j, 'topic', 'username', 'questions')

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

@app.route("/grade_test", methods=["POST"])
def grade_test():
    j = request.form.to_dict()
    validate_json(j, ['testName', 'username'])

    if 'file' not in request.files or request.files['file'].filename == '':
        print(request.files)
        raise InvalidUsage('You must provide a file for grading.')

    file = request.files['file']
    if file.content_type != 'image/jpeg':
        raise InvalidUsage('You must provide a valid JPG file; {} provided.'.format(file.content_type))

    # Save the file to a temporary directory
    project_dir = pythonWrapper.createProject('grading')
    print(project_dir)
    # Save the uploaded file to it
    file.save(path.join(project_dir, 'scans', 'to_grade.pdf'))

    # Regenerate test from saved JSON
    test_specs = retrieve_tests(j['testName'], j['username'])
    if not test_specs:
        raise InvalidUsage('No tests with the provided `testName` and `username` exist.',
                           status_code=404)
    test_spec = test_specs[0]

    tex_file_path = path.join(project_dir, 'text.tex')
    # Re-build the TeX file for the saved test
    with open(tex_file_path, mode='w') as quiz_file:
        quiz_file.write(parse_question_dict_list(test_spec['questions']))
        quiz_file.close()

    # Re-prepare questions and generate layout information
    pythonWrapper.prepareQuestion(project_dir, tex_file_path, 'TheNameOfThePDF')

    # Grade the tests using the layout information and get the path to the created zipfile
    # containing zooms + crops of the graded tests.
    zipfile_path = pythonWrapper.grade_uploaded_tests(project_dir)

    return send_file(zipfile_path, attachment_filename='zooms_and_crops.zip')

    # TODO: Cleanup temp dir

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(host='0.0.0.0', port=4545)
