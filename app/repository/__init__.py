from .mongo_repository import MongoRepository

import os

DB_ADDRESS = os.environ.get("DB_ADDRESS")
DB_NAME = os.environ.get("DB_NAME")

repository = MongoRepository(DB_ADDRESS, DB_NAME)