# backend_community_homework

[![CI](https://github.com/yandex-praktikum/hw03_forms/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw03_forms/actions/workflows/python-app.yml)


C:\\Users\\*NAME USER*\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m venv venv

C:\\Users\\tsa\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m venv venv

source venv/Scripts/activate

WARNING: You are using pip version 21.2.4;

python -m pip install --upgrade pip

pip install -r requirements.txt

pip freeze > requirements.txt

pip install pytest --upgrade 

pip install flake8-quotes

# Запуск сервера

python manage.py runserver

# Супер пользователь

python manage.py createsuperuser

#

# ----------------
# Миграция Базы 
# ----------------
# Первым делом запускается команда makemigrations, Django проверяет модели и таблицы в БД, анализирует их на соответствие друг другу, подготавливает скрипты миграций
#  и сообщает, какие миграции необходимо применить; однако никаких изменений в БД в этот момент не вносится.
# ----------------

python manage.py makemigrations

# Затем запускается команда migrate, и в этот момент все изменения вносятся в БД.

python manage.py migrate


Flake8

Выбрать и активировать нужный линтер можно с помощью командной строки VSC (Command Palette, вызывается через Ctrl+Shift+P).
Введите в командную строку Python: Select Linter и нажмите Enter.


новый проект
django-admin startproject имя_проекта

новое приложение

django-admin startapp имя_приложения

django-admin startapp api_yamdb
django-admin startapp users
django-admin startapp titles

 
yatube/static/



How to Use Python isort Library
https://simpleisbetterthancomplex.com/packages/2016/10/08/isort.html

Установка
Установите его через pip или возьмите код с GitHub:

pip install isort
Использование
Вы уже можете начать использовать его без какой-либо настройки:

Проверить и применить изменения везде
isort *

Показать изменения перед применением
isort * --diff

isort views.py urls.py

# show a diff before applying any change
isort views.py --diff

# just check for errors
isort urls.py --check-only


python manage.py test -v 2

python manage.py test posts.tests.test_views.PostContextTests.test_img

python manage.py test posts.tests.test_views.CommentAddTests.test_add_comment


Тестомерки Coverage
Проект не дымит. Что тестировать дальше?
Ответ на этот вопрос даст инструмент coverage (англ. «покрытие»). Он показывает, в какой степени код проекта проверен (покрыт) тестами.
Любимая игра программистов — увеличить coverage до 100%.
Установка пакета Coverage

pip3 install coverage

https://coverage.readthedocs.io/en/latest/index.html


# После выполнения команды 
coverage run --source='posts,users' manage.py test -v 2 
# coverage сформирует отчёт и сохранит его в корневой папке проекта, в файле .coverage.

# Самый простой способ — вывести результаты в консоль.
coverage report

# Для представления результатов есть и более удобный формат: отчёт можно сохранить в виде HTML.
coverage html

# Все команды отображения работают с созданным отчётом .coverage. После нового запуска 
coverage run 
# этот отчёт будет перезаписан.


Хозяйке на заметку: стандартный метод slugify из модуля django.utils.text не умеет работать с кириллицей. Нужно установить в виртуальное окружение пакет pytils (pip3 install pytils) и импортировать slugify именно из него, как это сделано в листинге deals/models.py


# ----------------
# Работа с графикой
# ----------------

# {Установка}
pip install pillow 
pip install sorl-thumbnail

# {Документация}
https://github.com/jazzband/sorl-thumbnail

# {Загрузка тегов библиотеки в шаблон}
<!-- Загрузка тегов библиотеки в шаблон -->
{% load thumbnail %}


<!-- Пример использования тега для пропорционального уменьшения и обрезки -->
<!-- картинки до размера 100x100px с центрированием -->
{% thumbnail item.image "100x100" crop="center" as im %}
  <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}">
{% endthumbnail %}


# ---!---!---!---!---!---!---!---!---!---!---!---!---!---

# ----------------
# Ошибки
# ----------------
# ModuleNotFoundError: No module named 'pip'
python -m ensurepip

# ----------------
# Миграция Базы
# ----------------
# Первым делом запускается команда makemigrations, Django проверяет модели и таблицы в БД, анализирует их на соответствие друг другу, подготавливает скрипты миграций
#  и сообщает, какие миграции необходимо применить; однако никаких изменений в БД в этот момент не вносится.
# ----------------

python manage.py makemigrations

# Затем запускается команда migrate, и в этот момент все изменения вносятся в БД.

python manage.py migrate

# ----------------
# установка django-debug-toolbar
# ----------------
pip install django-debug-toolbar