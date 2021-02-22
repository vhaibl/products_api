
Установка:

установить зависимости:
```shell
pip install -r requirements.txt
```
запустить БД
```shell
docker-compose up
```
сделать миграции и создать пользователя
```shell
./manage.py migrate
./manage.py createsuperuser
```
запустить сервер
```shell
./manage.py runserver
```

Автоматическая документация доступна по адресу http://127.0.0.1:8000/swagger/
Веб-интерфейс REST API по адресу http://127.0.0.1:8000/api/
  