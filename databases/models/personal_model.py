from datetime import datetime

from peewee import *

from .base_model import BaseModel


class PersonalModel(BaseModel):
    class Meta:
        table_name = 'Personal'

    id = PrimaryKeyField()
    name = CharField(unique=True)
    age = CharField(max_length=255, null=True)
    gender = CharField(max_length=255, null=True)
    height = CharField(max_length=255, null=True)
    skin_color = CharField(max_length=255, null=True)
    ethnicity = CharField(max_length=255, null=True)
    hair = CharField(max_length=255, null=True)
    profession = CharField(max_length=255, null=True)
    body_type = CharField(max_length=255, null=True)
    lifestyle = CharField(max_length=255, null=True)
    free_text = CharField(max_length=255, null=True)
    profile_picture = TextField(null=True)
    created_date = DateTimeField(default=datetime.now)
