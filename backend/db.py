""" Interfaces with MongoDB to store and load questions. """

import os
from typing import Callable, Optional, List

from pymongo import MongoClient

MONGO_USER = os.environ.get('MONGO_USER') or ''
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD') or ''
MONGO_HOST = os.environ.get('MONGO_HOST') or 'localhost'
MONGO_PORT = int(os.environ.get('MONGO_PORT')) if os.environ.get('MONGO_PORT') else 27017

MONGO_URL = "mongodb://{}{}{}{}{}:{}/".format(
    MONGO_USER,
    '' if MONGO_PASSWORD == '' else ':',
    MONGO_PASSWORD,
    '' if MONGO_USER == '' else '@',
    MONGO_HOST,
    MONGO_PORT
)

MONGO_CLIENT = MongoClient(MONGO_URL)
AMC_DB = MONGO_CLIENT["amc"]

def insert_questions(questions: List[dict], **kwargs):
    """ Inserts a list of questions into the database with a given topic. """

    questions_with_topics = map(lambda question: {**question, **kwargs}, questions)
    AMC_DB['questions'].insert_many(questions_with_topics)

def get_questions_by_topic(topic: str) -> List[dict]:
    """ Pulls all questions out of the dictinary with the supplied topic """

    res = AMC_DB['questions'].find({"topic": {"$eq": topic}})
    return list(res)

def remove_falsey_keys(dictionary: dict) -> dict:
    """ Removes all keys from the dictionary that are `None`, False, or an empty string. """

    is_truthy = lambda key: dictionary.get(key) not in (None, False, '',)
    truthy_keys = filter(is_truthy, dictionary.keys())
    return {key: dictionary[key] for key in truthy_keys}

def pluck(plucked_key: str) -> Callable[[dict], dict]:
    """ Returns a function that returns dictionary without a given key. """

    def pluck_inner(dictionary: dict) -> dict:
        """ Returns a dictionary without a given key. """
        return {key: dictionary[key] for key in filter(
            lambda key: key != plucked_key, dictionary.keys())}

    return pluck_inner

def remove_oids(docs: List[dict]) -> dict:
    """ Removes all `ObjectId` keys from the documents in the provided list of documents. """

    return list(map(pluck('_id'), docs))

def query_questions(topic: Optional[str], username: Optional[str],
                    question_text: Optional[List], limit=50) -> List[dict]:
    """ Returns all questions from the database that match the provided query, with a
    maximum of `limit`. """

    query = {
        'topic': topic,
        'username': username,
        'questionText': {'$regex': '.*{}.*'.format(question_text)} if question_text else None,
    }

    db_res = list(AMC_DB['questions'].find(remove_falsey_keys(query), limit=limit))
    return remove_oids(db_res)

def store_test(test_name: str, username: str, question_list: List[dict]):
    ''' Stores the questions and metadata used to generate a test in the database, making it
    possible to regenerate the test later for grading or other purposes. '''

    doc = {
        'name': test_name,
        'username': username,
        'questions': question_list,
    }

    AMC_DB['tests'].insert_one(doc)

def retrieve_tests(test_name: str, username: str) -> List[dict]:
    ''' Retrieves all tests that match the provided criteria, loading them from the database and
    converting them to JSON format. '''

    query = {
        'name': test_name,
        'username': username,
    }

    db_res = list(AMC_DB['tests'].find(query))
    return remove_oids(db_res)
