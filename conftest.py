import pytest
import allure
import requests
from urls import *
from data import *

@pytest.fixture
@allure.title('Фикстура создает пользователя с рандомными кредами и удаляет его из базы после прохождения теста')
def creating_new_user_and_delete():
    payload_cred = {
        'email' : generate_random_email(),
        'password' : generate_random_password(),
        'name' : generate_random_username()
    }
    response = requests.post(Urls.URL_user_register, data=payload_cred)
    response_body = response.json()

    yield payload_cred, response_body

    access_token = response_body['accessToken']
    requests.delete(Urls.URL_user_delete, headers={'Authorization': access_token})

@pytest.fixture
@allure.title('Фикстура создает пользователя и заказ на его аккаунт')
def creating_user_and_order_and_delete(creating_new_user_and_delete):
    access_token = creating_new_user_and_delete[1]['accessToken']
    headers = {'Authorization': access_token}
    payload = {'ingredients': [IngredientData.burger_2]}
    response_body = requests.post(Urls.URL_receive_user_orders, data=payload, headers=headers)

    yield access_token, response_body

    requests.delete(Urls.URL_user_delete, headers={'Authorization': access_token})