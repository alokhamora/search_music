# search_music

Приложение возвращет первую найденную песню и добавляет ее в базу данных.

Добавьте api_key из last.fm в API_KEY в global_var.py

Запуск: docker-compose up

Зарегистрировать пользователя: curl -d '{"name":"name_user", "mail": "mail", "password": "password"}' 0.0.0.0:8000/music/register

Отправить поисковый запрос: curl -u login:password '0.0.0.0:8000/music/search/?track=track_name'


