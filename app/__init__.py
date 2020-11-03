"""Setting environment variables

This is so that the application runs in dev mode,
since the production environment variables are set by 
the docker-compose file
"""
import os
os.environ["DB_ADDRESS"] = "mongodb://127.0.0.1:27017"
os.environ["DB_NAME"] = "api-register"