from .mongo_repository import MongoRepository

import os
DB_ADDRESS = os.environ.get("DB_ADDRESS", "mongodb://127.0.0.1:27017")
DB_NAME = os.environ.get("DB_NAME", "api-register")

repository = MongoRepository(DB_ADDRESS, DB_NAME)