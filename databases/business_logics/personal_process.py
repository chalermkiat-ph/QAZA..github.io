from ..models.personal_model import PersonalModel


class PersonalProcess:
    def __init__(self, db):
        self._db = db

        # create table
        with db.connection_context():
            db.create_tables([PersonalModel])

    def insert_data(self, personal_data):
        with self._db.atomic():
            PersonalModel.create(**personal_data)

    def get_all_data(self):
        result = []
        query = PersonalModel.select().order_by(PersonalModel.created_date.desc()).dicts()

        for row in query:
            result.append(row)

        return result

    def delete_data_by_id(self, id):
        query = PersonalModel.delete().where(PersonalModel.id == id)
        query.execute()  # Remove the rows, return number of rows removed.

    def get_data_by_criteria(self, criteria):
        criteria_str = ''
        for index, (key, value) in enumerate(criteria.items()):
            if value == '':
                continue
            if key == "age" or key == "height":
                if "-" in value:
                    list_value = value.split("-")
                    criteria_str = criteria_str + f'PersonalModel.{key}.between({list_value[0]}, {list_value[1]})'
                if "<" in value or ">" in value:
                    criteria_str = criteria_str + f'PersonalModel.{key} {value}'
            else:
                criteria_str = criteria_str + f'PersonalModel.{key} == "{value}"'

            if index == len(criteria) - 1:
                break
            criteria_str = criteria_str + ','

        query_str = f'PersonalModel.select().where({criteria_str})'

        result = []
        query = eval(query_str).dicts()

        for row in query:
            result.append(row)

        return result

        # if len(result) == 1:
        #     return result[0]
        #
        # # --------------------
        #
        # import random
        # index = random.randint(0, len(query))
        #
        # return result[index]