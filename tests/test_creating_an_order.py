from conftest import *

class TestOrderCreating:
    @allure.title('Проверка ответа при создании заказа с указанными ингредиентами для авторизованного пользователя')
    @allure.description('Выполняем два теста с разными наборами ингредиентов в бургере. '
                        'Аккаунт создается фикстурой перед тестом и удаляется после него.')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_order_creation_with_ingredients_authenticated(self, creating_new_user_and_delete, burger_ingredients):
        headers = {'Authorization': creating_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [burger_ingredients]}
        response = requests.post(Urls.URL_receiving_orders, data=payload, headers=headers)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['success'] is True
        assert 'name' in response_data
        assert 'number' in response_data['order']

    @allure.title('Проверка ответа при создании заказа с указанными ингредиентами для неавторизованного пользователя')
    @allure.description('Выполняем два теста с разными наборами ингредиентов в бургере.'
                        'Токен аккаунта не передается.')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_order_creation_no_ingredients_unauthenticate(self, burger_ingredients):
        payload = {'ingredients': [burger_ingredients]}
        response = requests.post(Urls.URL_receiving_orders, data=payload, headers=Urls.headers)
        assert {response.status_code == 401 and response.json() == 'success': False,'message': 'You should be authorised'}


    @allure.title('Проверка ответа при создании заказа без ингредиентов для авторизованного пользователя')
    @allure.description('Хеш ингредиента не передается в запросе. Аккаунт пользователя создается в фикстуре перед тестом.'
                        'После теста аккаунт удаляется.')
    def test_creating_an_order_no_ingredients_authorization_error(self, creating_new_user_and_delete):
        headers = {'Authorization': creating_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': []}
        response = requests.post(Urls.URL_receiving_orders, data=payload, headers=headers)
        assert response.status_code == 400 and response.json() == {'success': False, 'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа без ингредиентов для неавторизованного пользователя')
    @allure.description('Хеш ингредиента не передается в запросе. Токен аккаунта не передается в запросе.')
    def test_create_order_no_ingredients_unauthenticated_error(self):
        payload = {'ingredients': []}
        response = requests.post(Urls.URL_receiving_orders, data=payload, headers=Urls.headers)
        assert response.status_code == 400 and response.json() == {'success': False,'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа с неверным хешем ингредиента для авторизованного пользователя')
    @allure.description('Передан неверный хеш ингредиента. '
                        'Аккаунт пользователя создается в фикстуре перед тестом и удаляется после него.')
    def test_order_creation_invalid_hash_authenticated(self, creating_new_user_and_delete):
        headers = {'Authorization': creating_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [IngredientData.invalid_hash_ingredient]}
        response = requests.post(Urls.URL_receiving_orders, data=payload, headers=headers)
        assert response.status_code == 400 and response.json() == {'success': False,'message': 'One or more ids provided are incorrect'}