""" Interfaces with MongoDB to store and load questions. """

import os
from typing import List

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
