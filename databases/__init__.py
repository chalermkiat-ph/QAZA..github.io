from peewee import SqliteDatabase
from .business_logics.personal_process import PersonalProcess
from .models.base_model import *


class Databases(PersonalProcess):
    def __init__(self, database_file):
        # db = MySQLDatabase(database_name, host=host, port=port, user=user, password=password)
        db = SqliteDatabase(database_file)
        database_proxy.initialize(db)

        PersonalProcess.__init__(self, db)
