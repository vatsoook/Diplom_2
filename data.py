from helpers import *

class UsersData:
    email = 'ahmetdiv@ya.ru'
    password = '555666302'
    username = 'Vatsook'

    credentials_with_empty_field = [
        {'email': '',
         'password': generate_random_password(),
         'name': generate_random_username()
         },
        {'email': generate_random_email(),
         'password': '',
         'name': generate_random_username()
         },
        {'email': generate_random_email(),
         'password': generate_random_password(),
         'name': ''
         }
    ]

class IngredientData:
    burger_1 = ['61c0c5a71d1f82001bdaaa73', '61c0c5a71d1f82001bdaaa6c',
                '61c0c5a71d1f82001bdaaa76', '61c0c5a71d1f82001bdaaa79']

    burger_2 = ['61c0c5a71d1f82001bdaaa74', '61c0c5a71d1f82001bdaaa6d',
                '61c0c5a71d1f82001bdaaa7a', '61c0c5a71d1f82001bdaaa6f']

    invalid_hash_ingredient = '61c0c5a71d1f088005553535'