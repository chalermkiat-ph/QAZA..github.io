import base64
from databases import Databases

context = Databases('people.db')


with open("../files/1-8316618e.jpg", "rb") as image_file:
    # Convert to Base64
    base64_string = base64.b64encode(image_file.read()).decode('utf-8')


dict_personal = {
    'name': "ss",
    'age': 23,
    'gender': 'M',
    'height': 23,
    'skin_color': 'blue',
    'ethnicity': 'A',
    'hair': 23,
    'profession': 'Programmer',
    'body_type': 'fat',
    'lifestyle': 'sport',
    'free_text': 'i dont know',
    'profile_picture': base64_string,
}

context.personal_data_insert(dict_personal)