from conftest import *


class TestUserDataModification:
    user_data_update = {
        'email': generate_random_email(),
        'password': generate_random_password(),
        'name': generate_random_username()
    }

    @allure.title('Проверка успешного изменения данных пользователя при авторизации')
    def test_update_user_data_authenticated(self, creating_new_user_and_delete):
        response = requests.patch(Urls.URL_user_update, headers={
            'Authorization': creating_new_user_and_delete[1]['accessToken']}, data=TestUserDataModification.user_data_update)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['success'] is True
        assert response_data['user']['email'] == TestUserDataModification.user_data_update['email']
        assert response_data['user']['name'] == TestUserDataModification.user_data_update['name']

    @allure.title('Проверка ошибки при изменении данных неавторизованным пользователем')
    def test_update_user_data_unauthenticated(self):
        response = requests.patch(Urls.URL_user_update, headers=Urls.headers, data=TestUserDataModification.user_data_update)
        assert {response.status_code == 401 and response.json() == 'success': False, 'message': 'You should be authorised'}

