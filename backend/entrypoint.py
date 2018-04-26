""" Defines an API that can be used to interact with Auto Multiple Choice.  Exposes this
API via a HTTP interface using the Flask webserver. """

from os import path
from typing import List

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from tex_generation import parse_question_dict_list
import python_wrapper
from db import insert_questions, query_questions, store_test, retrieve_tests

app = Flask(__name__, static_url_path='')
CORS(app)

class InvalidUsage(Exception):
    ''' Indicates that the input provided to an API route is invalid, and that the request
    cannot be completed. '''

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict:
        ''' Converts this exception into a JSON-serializable dict suitable for being returned
        from an API route with an error status code. '''

        output = dict(self.payload or ())
        output['message'] = self.message
        output['success'] = False
        return output

@app.route("/", methods=["GET"])
def serve_index():
    ''' Serve the frontend at the root of the mountpoint. '''

    return app.send_static_file('index.html')


def validate_json(dictionary: dict, keys: List[str]):
    ''' Simple validation that just makes sure that all of the keys in the provided list
    exist in the provided dictionary. '''

    for key in keys:
        if not dictionary.get(key):
            raise InvalidUsage('You must supply a {} param.'.format(key))


@app.route("/create_project", methods=["POST"])
def generate_pdf():
    ''' Given the JSON specification for a test including the list of questions to be included
    in it and some other metadata and configuration, generates the test and returns the
    created PDF.

    The spec for the created test is stored in MongoDB so that it can be re-created later for
    grading. '''

    body = request.json
    validate_json(body, ['name', 'username', 'questions'])

    # Save the test definition to the database for later usage
    store_test(body['name'], body['username'], body['questions'])

    project_dir = python_wrapper.create_project(body['name'])
    print('Generated temporary project directory: {}'.format(project_dir))
    tex_file_path = path.join(project_dir, 'text.tex')

    with open(tex_file_path, mode='w') as quiz_file:
        quiz_file.write(parse_question_dict_list(body['questions'], copies=body.get('copies')))
        quiz_file.close()

    python_wrapper.prepare_question(project_dir, tex_file_path)

    pdf_path = path.join(project_dir, 'DOC-subject.pdf')

    # TODO: clean up project directory
    return send_file(pdf_path, attachment_filename='generated_quiz.pdf')


@app.route("/store_questions", methods=["POST"])
def store_questions():
    ''' Given a dictionary containing a username, topic, and list of questions to be stored, stores
    all of the questions in MongoDB for later retrieval and usage in generating quizzes. '''

    body = request.json
    validate_json(body, ['topic', 'username', 'questions'])

    insert_questions(body['questions'], topic=body['topic'], username=body['username'])

    return jsonify({
        "success": True,
        "message": "Questions successfully stored."
    })


@app.route("/find_questions", methods=["POST"])
def find_questions():
    ''' Given a query, returns all questions in the MongoDB that match it. '''

    body = request.json
    db_res = query_questions(body.get('topic'), body.get('username'), body.get('question_text'))
    return jsonify(db_res)


@app.route("/grade_test", methods=["POST"])
def grade_test():
    ''' Given an uploaded PDF file as well as the username and topic of a previously generated
    quiz, regenerates the project directory for the quiz and grades the uploaded scan.  The
    directory containing zooms, crops, and the final grade CSV is zipped and send back to the
    user. '''

    body = request.form.to_dict()
    validate_json(body, ['testName', 'username'])

    if 'file' not in request.files or request.files['file'].filename == '':
        print(request.files)
        raise InvalidUsage('You must provide a file for grading.')

    file = request.files['file']
    if file.content_type != 'image/jpeg':
        raise InvalidUsage(
            'You must provide a valid JPG file; {} provided.'.format(file.content_type))

    # Save the file to a temporary directory
    project_dir = python_wrapper.create_project('grading')
    print(project_dir)
    # Save the uploaded file to it
    file.save(path.join(project_dir, 'scans', 'to_grade.pdf'))

    # Regenerate test from saved JSON
    test_specs = retrieve_tests(body['testName'], body['username'])
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
    python_wrapper.prepare_question(project_dir, tex_file_path)

    # Grade the tests using the layout information and get the path to the created zipfile
    # containing zooms + crops of the graded tests.
    zipfile_path = python_wrapper.grade_uploaded_tests(project_dir)

    return send_file(zipfile_path, attachment_filename='zooms_and_crops.zip')

    # TODO: Cleanup temp dir


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    ''' This handler is triggered whenever any of the other API routes raise an `InvalidUsage`
    exception.  The error is returned to the user with an error status code. '''

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(host='0.0.0.0', port=4545)
