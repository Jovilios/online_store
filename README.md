# X Store

X Store is a marketplace for fast sales of both brand new and used items.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)


# Features


# Installation:

To ensure proper and correct operation of the project, you must install the requirements.txt file. Your computer should have PostgresSQL and Redis installed.

1. Start by installing PostgresSQL and Redis.

2. Then, install the necessary packages using <code>pip install -r requirements.txt</code>

3. Next, run migrations with <code>python manage.py makemigrations</code> and <code>python manage.py migrate</code>.

4. To run the project correctly, start the server with <code>python manage.py runserver</code> and <code>celery with celery -A online_store worker --loglevel=info -P eventlet -E</code>