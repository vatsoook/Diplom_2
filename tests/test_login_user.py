from conftest import *

class TestUserAuthentication:

    @allure.title('Проверка успешной аутентификации пользователя с корректными учетными данными')
    @allure.description('Аутентификация осуществляется с помощью фикстуры, создающей аккаунт для тестирования. '
                        'После теста аккаунт удаляется. Проверяются код ответа и тело, а также получение accessToken и refreshToken.')
    def test_successful_login_with_existing_account(self, creating_new_user_and_delete):
        credentials = creating_new_user_and_delete[0]
        response = requests.post(Urls.URL_user_auth, data=credentials)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['success'] is True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert response_data['user']['email'] == creating_new_user_and_delete[0]['email']
        assert response_data['user']['name'] == creating_new_user_and_delete[0]['name']

    @allure.title('Проверка ошибки аутентификации при неверном email')
    def test_login_with_invalid_email(self):
        credentials = {
            'email': generate_random_email(),
            'password': UsersData.password,
        }
        response = requests.post(Urls.URL_user_auth, data=credentials)
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'email or password are incorrect'}

    @allure.title('Проверка ошибки аутентификации при неверном пароле')
    def test_login_with_invalid_password(self):
        credentials = {
            'email': UsersData.email,
            'password': generate_random_password(),
        }
        response = requests.post(Urls.URL_user_auth, data=credentials)
        assert response.status_code == 401 and response.json() == {'success': False, 'message': 'email or password are incorrect'}