# Проект YaMDB

### Описание 
Проект YaMDB собирает отзывы пользователей на произведения (книги, фильмы, музыку). Сами произведения здесь не хранятся. Незарегистрированные пользователи могут просматривать информацию о произведениях, жанрах и категориях произведений, а также читать отзывы и комментарии.
Зарегистрированные пользователи могут оставлять отзывы и комментарии на произведения, а также выставлять оценку от 1 до 10. Право добавлять произведения, жанры и категории есть только у администраторов проекта. 

----

### В API доступны следующие эндпоинты:

* ```http://127.0.0.1:8000/api/v1/auth/signup/``` POST-запрос — получение кода подтверждения (confirmation_code) на указанный email.

* ```http://127.0.0.1:8000/api/v1/auth/token/``` POST-запрос — получение Access-токена в обмен на username и confirmation_code.

* ```http://127.0.0.1:8000/api/v1/users/``` Доступно для пользователей с ролью "администратор".
GET-запрос — получение списка всех пользователей, POST-запрос — добавление нового пользователя.

* ```http://127.0.0.1:8000/api/v1/users/{username}/``` Доступно для пользователей с ролью "администратор".
GET-запрос — получение пользователя по username.
PATCH-запрос — редактирование данных пользователя. DELETE-запрос — удаление пользователя.

* ```http://127.0.0.1:8000/api/v1/users/me/``` Права доступа — любой зарегистрированный пользователь.
GET-запрос — получение данных о своей учётной записи. PATCH-запрос — редактирование своей учётной записи.
Изменить роль пользователя нельзя.

* ```http://127.0.0.1:8000/api/v1/categories/``` GET-запрос — получение списка всех категорий (доступно без токена).
POST-запрос — создание новой категории (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/categories/{slug}/``` Доступно для пользователей с ролью "администратор".
DELETE-запрос — удаление категории по её slug.

* ```http://127.0.0.1:8000/api/v1/genres/``` GET-запрос — получение списка всех жанров (доступно без токена).
POST-запрос — добавление нового жанра (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/genres/{slug}/``` Доступно для пользователей с ролью "администратор".
DELETE-запрос — удаление жанра по его slug.

* ```http://127.0.0.1:8000/api/v1/titles/``` GET-запрос — получение списка всех произведений (доступно без токена).
POST-запрос — добавление нового произведения (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/titles/{titles_id}/``` GET-запрос — получение информации о произведении (доступно без токена).
PATCH-запрос — обновление информации о произведении (доступно для администратора).
DELETE-запрос — удаление произведения (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/``` GET-запрос — получение списка всех отзывов (доступно без токена).
POST-запрос — добавление нового отзыва (доступно для аутентифицированных пользователей). Пользователь может оставить один отзыв на произведение.

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/``` GET-запрос — получение отзыва о произведении по его id (доступно без токена).
PATCH-запрос — изменение отзыва (доступно для администратора, модератора и автора отзыва).
DELETE-запрос — удаление отзыва по id (доступно для модератора, администратора и автора отзыва).

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/``` GET-запрос — получение списка комментариев к отзыву (доступно без токена).
POST-запрос — добавление комментария к отзыву (доступно для аутентифицированных пользователей). 

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/``` GET-запрос — получение информации о комментарии по id (доступно без токена).
PATCH-запрос — частичное обновление комментария (доступно для администратора, модератора и автора комментария).
DELETE-запрос — удаление комментария (доступно для администратора, модератора и автора комментария).

----

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/mariyabykova/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
----

### Как импортировать данные из csv-файлов в базу данных

Предусмотрены два способа загрузки данных из csv-файлов:

* Через админ-панель (использована библиотека django-import-export).
* С помощью management-команд. Для этого из корневой директории проекта выполните команду:

```
python3 manage.py <название файла с management-командой> --path <путь к csv-файлу>
```

Например, для импорта данных о пользователях из файла 'users.csv' команда будет следующей:

```
python3 manage.py load_user_data --path static/data/users.csv
```

----

### Авторы проекта

**Мария Быкова.** Тимлид. Регистрация и авторизация, управление пользователями, права доступа.

**Михаил Буланкин.** Произведения, категории, жанры, импорт csv-файлов.

**Владислав Гордин.** Отзывы, комментарии, рейтинг произведений.
