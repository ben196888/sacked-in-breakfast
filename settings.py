import os
import pymongo

DB = pymongo.Connection()["sacked"]
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
