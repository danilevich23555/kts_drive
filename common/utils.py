import os


def show_api_url():
    if not os.environ.get('API_EXPOSER_URL'):
        print('В переменных окружения нет ссылки на развернутое API, пожалуйста, напишите в чат группы')
    else:
        print(f'Запущенный сервер доступен по этой ссылке: {os.environ["API_EXPOSER_URL"]}')
