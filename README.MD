<h1 align="center">Китос, привет ептвую мать 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

>Запуск приложения:
>>Запустить в терминале команду docker-compose up;
>>>Перейдите по адресу: http://127.0.0.1:9001/buckets и создать ведро "kts-drive", логин и пароль minioadmin
>>>>Установить зависимости запустив команду в терминале pip install -r rquirements.txt
>>>>>Накатить миграции в БД выполнив команду в терминале "alembic upgrade head"
>>>>>>Запустить файл drive_server/main.py
>>>>>>>Через postman создать юзера endpoint http://0.0.0.0:8888/adduser со следующим json файлом {
"username": "25@yandex.ru",
"password": "wishoting"} данные могут быть любые
>>>>>>>>Перейти на адрес http://0.0.0.0:8888 и авторизироваться с созданным пользователем
>>>>>>>>> Можно загружать файлы и они будут перекачиваться в s3minio