# deal project


### Запускаем проект локально
- клонируем репозиторий:
- `git clone https://github.com/baigashl/deal_proj.git`


- заходим в проект:
- `cd deal_proj`


- создаем .env файл с ключами:
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT
- DEBUG
- USE_S3


- запуск с помощью docker:
- `docker-compose up -d --build`



- создаем суперюзера:
- `docker-compose exec backend bash`
- `cd backend`
- `python manage.py migrate`
- `python manage.py createsuperuser`



- переходим по ссылке (админ панель):
- http://localhost/admin/
- 
- документация swagger:
- http://localhost:8000/swagger-ui/


- Api для загрузки csv файла
- http://localhost:8000/deal/uploadfile/
-
- список из 5 клиентов, потративших наибольшую сумму за весь период.
- http://localhost:8000/deal/list/





