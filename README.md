# REST API для бронирования отелей

Этот проект представляет собой REST API, созданный с использованием FastAPI для бронирования отелей.

## Особенности

- Аутентификация и авторизация пользователей
- Поиск отелей и возможность их бронирования
- Просмотр и изменение существующих бронирований
- Панель администратора для управления отелями и бронированиями

## Начало работы

Для запуска этого проекта локально убедитесь, что у вас установлен Docker на вашем компьютере. Склонируйте этот репозиторий и перейдите в директорию проекта.

git clone https://github.com/HardyITM/hotel_booking.git
cd project-directory


Далее, необходимо заполнить файл .env в директории проекта


После установки переменных окружения, вы можете запустить приложение с помощью Docker Compose:

docker-compose up


API будет доступно по адресу http://localhost:8000, а Swagger UI для тестирования по адресу http://localhost:8000/docs.

## Миграции базы данных

Если вам нужно внести изменения в схему базы данных, вы можете создать новую миграцию с помощью Alembic:

docker-compose exec web alembic revision --autogenerate -m "Ваше сообщение миграции"
docker-compose exec web alembic upgrade head


## Документация API

Вы можете найти документацию API и его эндпоинты в Swagger UI по адресу http://localhost:8000/docs.