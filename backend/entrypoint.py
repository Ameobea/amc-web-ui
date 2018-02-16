import json

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/example_json_post", methods=["POST"])
def process_question():
    print(request.json)

    body = request.json
    body['a'] = body['a'] + 1

    return json.dumps(body)

app.run(port=4545)
