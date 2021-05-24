# Yatube - социальная сеть
## Описание
Мой первый учебный проект на пути к Python Developer. Доступен по адресу https://yatube.rusich90.ru/

Для создания были использованы и изучены:

* Python
* Django
* REST API
* SQL
* HTML
* JWT Token
* smtp gmail
* Linux
* Gunicorn, NGINX
* Удаленный сервер, доменные имена, SSL сертификаты
* Тестирование кода

Возможности:

* Публиковать, просматривать, изменять, удалять и комментировать посты
* Подписываться на авторов
* Загружать фотографии
* Просматривать и создавать группы.
* Комментировать, смотреть, удалять и обновлять комментарии.

Так же реализован REST API, документация доступна по адресу https://yatube.rusich90.ru/redoc/

## Установка 
Клонируем репозиторий на локальную машину:

```$ git clone https://github.com/Rusich90/yatube.git```

 Создаем виртуальное окружение:
 
 ```$ python -m venv venv```
 
  Активируем виртуальное окружение
 
 ```$ source venv/Scripts/activate```
 
 Переходм в папку polls
 
 ```$ cd yatube/```
 
 Устанавливаем зависимости:

```$ pip install -r requirements.txt```

Создание и применение миграций:

```$ python manage.py makemigrations``` и ```$ python manage.py migrate```

Запускаем django сервер:

```$ python manage.py runserver```

Для подключения почтовой рассылки и мониторинга Sentry нужно создать файл .env (с секретными данными) в директории с settings.py и в самом settings.py раскомментировать настройки Sentry и почтового хоста.
