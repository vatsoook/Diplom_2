from conftest import *
import requests

class TestUserOrdersRetrieval:

    @allure.title('Проверка успешного получения списка заказов для авторизованного пользователя')
    @allure.description('Перед тестом создается аккаунт и заказ, после чего тест получает список заказов, а аккаунт удаляется из базы данных')
    def test_successful_order_retrieval_authenticated_user(self, creating_user_and_order_and_delete):
        headers = {'Authorization': creating_user_and_order_and_delete[0]}
        response = requests.get(Urls.URL_receive_user_orders, headers=headers)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['success'] is True
        assert 'orders' in response_data
        assert 'total' in response_data

    @allure.title('Проверка ошибки при получении списка заказов для неавторизованного пользователя')
    def test_order_retrieval_unauthenticated_user(self):
        response = requests.get(Urls.URL_receive_user_orders, headers=Urls.headers)
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'You should be authorised'}