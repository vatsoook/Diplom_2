class Urls:
    URL_basic = 'https://stellarburgers.nomoreparties.site'
    URL_user_register = f'{URL_basic}/api/auth/register'
    URL_user_auth = f'{URL_basic}/api/auth/login'
    URL_user_update = f'{URL_basic}/api/auth/user'
    URL_user_delete = f'{URL_basic}/api/auth/user'
    URL_receiving_orders = f'{URL_basic}/api/orders'
    URL_receive_user_orders = f'{URL_basic}/api/orders'

    headers = {'Content-Type': 'application/json'}