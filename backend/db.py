""" Interfaces with MongoDB to store and load questions. """

import json
import os
from typing import Callable, Optional, List

from pymongo import MongoClient

MONGO_USER = os.environ.get('MONGO_USER') or ''
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD') or ''
MONGO_HOST = os.environ.get('MONGO_HOST') or 'localhost'
MONGO_PORT = int(os.environ.get('MONGO_PORT')) if os.environ.get('MONGO_HOST') else 27017

mongo_url = "mongodb://{}{}{}{}{}:{}/".format(
    MONGO_USER,
    '' if MONGO_PASSWORD == '' else ':',
    MONGO_PASSWORD,
    '' if MONGO_USER == '' else '@',
    MONGO_HOST,
    MONGO_PORT
)

mongo_client = MongoClient(mongo_url)
amc_database = mongo_client["amc"]

def insert_questions(questions: List[dict], **kwargs):
    """ Inserts a list of questions into the database with a given topic. """

    questions_with_topics = map(lambda question: {**question, **kwargs}, questions)
    amc_database['questions'].insert_many(questions_with_topics)

def get_questions_by_topic(topic: str) -> List[dict]:
    """ Pulls all questions out of the dictinary with the supplied topic """

    res = amc_database['questions'].find({"topic": {"$eq": topic}})
    return list(res)

def remove_falsey_keys(d: dict) -> dict:
    """ Removes all keys from the dictionary that are `None`, False, or an empty string. """

    truthy_keys = filter(lambda key: d.get(key) not in (None, False, '',), d.keys())
    return {key: d[key] for key in truthy_keys}

def pluck(plucked_key: str) -> Callable[[dict], dict]:
    """ Returns a function that returns dictionary without a given key. """

    def pluck_inner(d: dict) -> dict:
        """ Returns a dictionary without a given key. """
        return {key: d[key] for key in filter(lambda key: key != plucked_key, d.keys())}

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

    db_res = list(amc_database['questions'].find(remove_falsey_keys(query), limit=limit))
    return remove_oids(db_res)
