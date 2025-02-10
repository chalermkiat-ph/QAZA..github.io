from .api import personal_api


class PersonalAPI:
    def __init__(self, database_file):
        personal_api.DatabaseConfig = database_file
