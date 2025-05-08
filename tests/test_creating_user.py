import allure
import requests
from data import *
from urls import *
import pytest


class TestUserRegistration:
    @allure.title('Проверка успешной регистрации пользователя с корректными данными')
    @allure.description('Создание аккаунта с использованием данных, генерируемых библиотекой Faker. '
                        'После теста аккаунт удаляется из базы данных. Проверяются код ответа и тело, а также получение accessToken и refreshToken.')
    def test_user_registration_successful(self):
        user_data = {
            'email': generate_random_email(),
            'password': generate_random_password(),
            'name': generate_random_username()
        }

        response = requests.post(Urls.URL_user_register, data=user_data)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['success'] is True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert response_data['user']['email'] == user_data['email']
        assert response_data['user']['name'] == user_data['name']

        access_token = response_data['accessToken']
        requests.delete(Urls.URL_user_delete, headers={'Authorization': access_token})

    @allure.title('Проверка ответа при регистрации уже существующего пользователя')
    @allure.description('Попытка регистрации с данными уже зарегистрированного пользователя. '
                        'Если аккаунт создается, он удаляется после теста.')
    def test_registration_existing_user(self):
        user_data = {
            'email': UsersData.email,
            'password': generate_random_password(),
            'name': generate_random_username()
        }
        response = requests.post(Urls.URL_user_register, data=user_data)
        assert response.status_code == 403
        assert response.json() == {'success': False, 'message': 'User already exists'}


    @allure.title('Проверка ответа при регистрации с незаполненными обязательными полями')
    @allure.description('Тесты, где не заполнено одно из полей — email, password или name.'
                        'Если аккаунт создается, он удаляется после теста.')
    @pytest.mark.parametrize('user_credentials', UsersData.credentials_with_empty_field)
    def test_create_user_the_field_is_not_filled_in_failed(self, user_credentials):
        response = requests.post(Urls.URL_user_register, data=user_credentials)
        assert (response.status_code == 403 and response.json() == {'success': False, 'message': 'Email, password and name are required fields'})